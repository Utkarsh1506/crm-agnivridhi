from django.urls import path
from . import views

# Namespace for reverse() calls like 'documents:document_detail'
app_name = 'documents'

urlpatterns = [
    # Role-specific document pages
    path('', views.document_list, name='document_list'),  # deprecated generic -> redirects
    path('client/', views.client_documents_list, name='client_documents_list'),
    path('client/upload/', views.client_document_upload, name='client_document_upload'),
    path('sales/', views.sales_documents_list, name='sales_documents_list'),
    path('sales/checklist/create/<int:client_id>/', views.sales_create_checklist, name='sales_create_checklist'),
    path('sales/uploads/', views.sales_client_uploads_list, name='sales_client_uploads_list'),
    path('sales/upload/', views.sales_upload_for_client, name='sales_upload_document'),
    path('sales/upload/<int:client_id>/', views.sales_upload_for_client, name='sales_upload_for_client'),
    path('team/', views.team_documents_list, name='team_documents_list'),
    path('team/checklist/create/<int:client_id>/', views.manager_create_checklist, name='manager_create_checklist'),
    path('team/uploads/', views.team_client_uploads_list, name='team_client_uploads_list'),

    # Detail and download
    path('<int:pk>/', views.document_detail, name='document_detail'),
    path('<int:pk>/download/', views.document_download, name='document_download'),
]
