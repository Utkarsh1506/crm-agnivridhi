from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.contrib import messages
from .models import Document
from accounts.views import manager_required, client_required, sales_required
from .forms import DocumentUploadForm, SalesDocumentUploadForm
from .models import DocumentChecklist
from clients.models import Client

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
    # using imported DocumentChecklist and Client
    
    # Get clients for this sales user
    clients = Client.objects.filter(
        Q(assigned_sales=request.user) | Q(created_by=request.user)
    ).select_related('assigned_sales').order_by('company_name')
    
    # Group documents and checklists by client
    client_data = []
    for client in clients:
        # Get checklist for this client
        checklist = DocumentChecklist.objects.filter(client=client).select_related('uploaded_document')
        
        # Get client uploaded documents (role=CLIENT)
        uploaded_docs = Document.objects.filter(
            client=client,
            generated_by__role='CLIENT'
        ).select_related('generated_by').order_by('-created_at')
        
        # Calculate progress
        total_required = checklist.filter(is_required=True).count()
        uploaded_required = checklist.filter(is_required=True, is_uploaded=True).count()
        progress = int((uploaded_required / total_required) * 100) if total_required > 0 else 0
        
        client_data.append({
            'client': client,
            'checklist': checklist,
            'uploaded_docs': uploaded_docs,
            'total_required': total_required,
            'uploaded_required': uploaded_required,
            'progress': progress,
        })
    
    context = {
        'client_data': client_data,
    }
    return render(request, 'documents/sales_documents_with_checklist.html', context)


@sales_required
def sales_create_checklist(request, client_id):
    """Create default checklist items for a client (Sales/Manager can use Sales route)."""
    client = get_object_or_404(Client, pk=client_id)
    # Permission: sales who owns client OR manager assigned to client OR admin/owner
    user = request.user
    user_role = getattr(user, 'role', '').upper()
    if not (
        client.assigned_sales == user or
        client.created_by == user or
        client.assigned_manager == user or
        user_role in ['ADMIN', 'OWNER'] or getattr(user, 'is_superuser', False)
    ):
        messages.error(request, "You don't have permission to create a checklist for this client.")
        return redirect('documents:sales_documents_list')

    # Preset required document types
    required_types = [
        Document.DocumentType.PAN_CARD,
        Document.DocumentType.GST_CERT,
        Document.DocumentType.COMPANY_REG,
        Document.DocumentType.BANK_STATEMENT,
        Document.DocumentType.ITR,
        Document.DocumentType.BALANCE_SHEET,
    ]
    optional_types = [
        Document.DocumentType.MSME_CERT,
        Document.DocumentType.MOA_AOA,
        Document.DocumentType.BOARD_RESOLUTION,
    ]

    created_count = 0
    for dt in required_types:
        obj, created = DocumentChecklist.objects.get_or_create(
            client=client,
            document_type=dt,
            defaults={
                'is_required': True,
                'created_by': user,
            }
        )
        if created:
            created_count += 1
    for dt in optional_types:
        obj, created = DocumentChecklist.objects.get_or_create(
            client=client,
            document_type=dt,
            defaults={
                'is_required': False,
                'created_by': user,
            }
        )
        if created:
            created_count += 1

    if created_count > 0:
        messages.success(request, f'Document checklist created/updated for {client.company_name}.')
    else:
        messages.info(request, f'Checklist already exists for {client.company_name}.')

    return redirect('documents:sales_documents_list')


@manager_required
def manager_create_checklist(request, client_id):
    """Create default checklist items for a client from Manager dashboard."""
    client = get_object_or_404(Client, pk=client_id)
    user = request.user

    # Permission: assigned manager, creator, admin/owner, or superuser
    user_role = getattr(user, 'role', '').upper()
    if not (
        client.assigned_manager == user or
        client.created_by == user or
        user_role in ['ADMIN', 'OWNER'] or getattr(user, 'is_superuser', False)
    ):
        messages.error(request, "You don't have permission to create a checklist for this client.")
        return redirect('documents:team_documents_list')

    required_types = [
        Document.DocumentType.PAN_CARD,
        Document.DocumentType.GST_CERT,
        Document.DocumentType.COMPANY_REG,
        Document.DocumentType.BANK_STATEMENT,
        Document.DocumentType.ITR,
        Document.DocumentType.BALANCE_SHEET,
    ]
    optional_types = [
        Document.DocumentType.MSME_CERT,
        Document.DocumentType.MOA_AOA,
        Document.DocumentType.BOARD_RESOLUTION,
    ]

    created_count = 0
    for dt in required_types:
        _, created = DocumentChecklist.objects.get_or_create(
            client=client,
            document_type=dt,
            defaults={'is_required': True, 'created_by': user}
        )
        if created:
            created_count += 1
    for dt in optional_types:
        _, created = DocumentChecklist.objects.get_or_create(
            client=client,
            document_type=dt,
            defaults={'is_required': False, 'created_by': user}
        )
        if created:
            created_count += 1

    if created_count > 0:
        messages.success(request, f'Document checklist created/updated for {client.company_name}.')
    else:
        messages.info(request, f'Checklist already exists for {client.company_name}.')

    return redirect('documents:team_documents_list')


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


@sales_required
def sales_upload_for_client(request, client_id=None):
    """Allow sales employees to upload documents for their assigned clients"""
    from clients.models import Client
    from django.db.models import Q
    
    # Get client if client_id provided, otherwise None
    client = None
    if client_id:
        client = get_object_or_404(Client, pk=client_id)
        # Verify this sales user has access to this client
        if not (client.assigned_sales == request.user or client.created_by == request.user):
            messages.error(request, "You don't have permission to upload documents for this client.")
            return redirect('documents:sales_client_uploads_list')
    
    if request.method == 'POST':
        form = SalesDocumentUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            doc: Document = form.save(commit=False)
            doc.generated_by = request.user
            doc.status = Document.Status.GENERATED
            doc.save()
            messages.success(request, f'Document uploaded successfully for {doc.client.company_name}.')
            return redirect('documents:sales_client_uploads_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-populate client field if client_id provided
        if client:
            form = SalesDocumentUploadForm(user=request.user, initial={'client': client})
        else:
            form = SalesDocumentUploadForm(user=request.user)
    
    context = {
        'form': form,
        'client': client,
    }
    return render(request, 'documents/sales_upload_document.html', context)
