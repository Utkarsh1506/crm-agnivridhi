from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.contrib import messages
from .models import Document
from accounts.views import manager_required, client_required, sales_required

@login_required
def document_list(request):
    """Deprecated generic endpoint: redirect to role-specific page for privacy."""
    user = request.user
    if getattr(user, 'is_client', False):
        return redirect('client_documents_list')
    elif getattr(user, 'role', None) == 'SALES':
        return redirect('sales_documents_list')
    elif getattr(user, 'role', None) in ['MANAGER', 'ADMIN']:
        return redirect('team_documents_list')
    return redirect('dashboard')


@client_required
def client_documents_list(request):
    client = request.user.client_profile
    documents = Document.objects.filter(client=client).order_by('-created_at')
    return render(request, 'documents/document_list.html', {'documents': documents})


@sales_required
def sales_documents_list(request):
    # Documents for clients assigned to this sales user
    documents = Document.objects.filter(client__assigned_sales=request.user).order_by('-created_at')
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
