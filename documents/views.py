from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.contrib import messages
from .models import Document
from accounts.views import manager_required, client_required, sales_required
from .forms import DocumentUploadForm

@login_required
def document_list(request):
    """Deprecated generic endpoint: redirect to role-specific page for privacy."""
    user = request.user
    if getattr(user, 'is_client', False):
        return redirect('documents:client_documents_list')
    elif getattr(user, 'role', None) == 'SALES':
        return redirect('documents:sales_documents_list')
    elif getattr(user, 'role', None) in ['MANAGER', 'ADMIN']:
        return redirect('documents:team_documents_list')
    return redirect('dashboard')


@client_required
def client_documents_list(request):
    client = request.user.client_profile
    from django.db.models import Q
    qs = Document.objects.filter(client=client).select_related('application', 'booking', 'generated_by').order_by('-created_at')
    my_uploads = qs.filter(generated_by=request.user)
    shared_documents = qs.exclude(generated_by=request.user)
    context = {
        'documents': qs,  # backward compatibility for templates expecting 'documents'
        'my_uploads': my_uploads,
        'shared_documents': shared_documents,
    }
    return render(request, 'documents/document_list.html', context)


@client_required
def client_document_upload(request):
    """Allow clients to upload their own documents"""
    client = request.user.client_profile
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc: Document = form.save(commit=False)
            doc.client = client
            doc.generated_by = request.user
            # Mark as generated/available once uploaded
            doc.status = Document.Status.GENERATED
            doc.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('documents:client_documents_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DocumentUploadForm()
    return render(request, 'documents/document_upload.html', {'form': form})


@sales_required
def sales_documents_list(request):
    # Documents for clients assigned to this sales user or created by them
    from django.db.models import Q
    documents = Document.objects.filter(
        Q(client__assigned_sales=request.user) | Q(client__created_by=request.user)
    ).select_related('client', 'application', 'booking').order_by('-created_at')
    return render(request, 'documents/document_list.html', {'documents': documents})


@sales_required
def sales_client_uploads_list(request):
    """Sales view: Only documents uploaded by clients (their assigned/created clients)."""
    from django.db.models import Q
    documents = Document.objects.filter(
        Q(client__assigned_sales=request.user) | Q(client__created_by=request.user),
        Q(generated_by__role='CLIENT')
    ).select_related('client', 'application', 'booking', 'generated_by').order_by('-created_at')
    return render(request, 'documents/document_list.html', {'documents': documents})


@manager_required
def team_documents_list(request):
    """Manager/Admin view: Documents for team clients; Admin/Owner sees all."""
    user = request.user
    
    # Get all clients assigned to this manager's team or all for admin/owner
    from clients.models import Client
    user_role = getattr(user, 'role', '').upper()
    if user_role in ['ADMIN', 'OWNER'] or getattr(user, 'is_superuser', False):
        team_clients = Client.objects.all().select_related('assigned_sales', 'assigned_manager')
        documents = Document.objects.all().select_related('client', 'client__assigned_sales', 'generated_by').order_by('-created_at')
    else:
        team_clients = Client.objects.filter(assigned_manager=user).select_related('assigned_sales', 'assigned_manager')
        
        # Get documents for these clients
        documents = Document.objects.filter(client__in=team_clients).select_related('client', 'client__assigned_sales', 'generated_by').order_by('-created_at')
    
    # Group by client
    documents_by_client = {}
    for doc in documents:
        client_name = doc.client.company_name
        if client_name not in documents_by_client:
            documents_by_client[client_name] = {
                'client': doc.client,
                'documents': []
            }
        documents_by_client[client_name]['documents'].append(doc)
    
    context = {
        'documents': documents,
        'documents_by_client': documents_by_client,
        'total_documents': documents.count(),
        'total_clients': team_clients.count(),
    }
    return render(request, 'documents/team_documents_list.html', context)


@manager_required
def team_client_uploads_list(request):
    """Manager/Admin view: Only documents uploaded by clients (team or all)."""
    user = request.user
    from django.db.models import Q
    from clients.models import Client
    user_role = getattr(user, 'role', '').upper()
    if user_role in ['ADMIN', 'OWNER'] or getattr(user, 'is_superuser', False):
        documents = Document.objects.filter(generated_by__role='CLIENT').select_related('client', 'client__assigned_sales', 'generated_by').order_by('-created_at')
        team_clients = Client.objects.all()
    else:
        team_clients = Client.objects.filter(assigned_manager=user)
        documents = Document.objects.filter(client__in=team_clients, generated_by__role='CLIENT').select_related('client', 'client__assigned_sales', 'generated_by').order_by('-created_at')

    # Group by client
    documents_by_client = {}
    for doc in documents:
        client_name = doc.client.company_name
        if client_name not in documents_by_client:
            documents_by_client[client_name] = {
                'client': doc.client,
                'documents': []
            }
        documents_by_client[client_name]['documents'].append(doc)

    context = {
        'documents': documents,
        'documents_by_client': documents_by_client,
        'total_documents': documents.count(),
        'total_clients': team_clients.count(),
    }
    return render(request, 'documents/team_documents_list.html', context)


@login_required
def document_detail(request, pk):
    """View document details"""
    document = get_object_or_404(Document, pk=pk)
    
    # Check permissions
    user = request.user
    if user.is_client and document.client.user != user:
        messages.error(request, "You don't have permission to view this document.")
        return redirect('document_list')
    
    context = {
        'document': document,
    }
    return render(request, 'documents/document_detail.html', context)

@login_required
def document_download(request, pk):
    """Download document file"""
    document = get_object_or_404(Document, pk=pk)
    
    # Check permissions
    user = request.user
    if user.is_client and document.client.user != user:
        raise Http404("Document not found")
    
    # Record download
    document.record_download(user)
    
    # Serve file
    try:
        return FileResponse(document.file.open('rb'), as_attachment=True, filename=document.file.name)
    except Exception as e:
        messages.error(request, f"Error downloading file: {str(e)}")
        return redirect('document_detail', pk=pk)
