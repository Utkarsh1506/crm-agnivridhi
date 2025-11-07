from django.urls import path
from . import views

app_name = 'edit_requests'

urlpatterns = [
    # Sales - Request edit
    path('client/<int:client_id>/request-edit/', views.request_client_edit, name='request_client_edit'),
    
    # Manager - View and approve/reject requests
    path('manager/pending/', views.manager_edit_requests, name='manager_edit_requests'),
    path('<int:request_id>/approve/', views.approve_edit_request, name='approve_edit_request'),
    path('<int:request_id>/reject/', views.reject_edit_request, name='reject_edit_request'),
    
    # Manager - Direct edit (no approval needed)
    path('client/<int:client_id>/edit/', views.edit_client_direct, name='edit_client_direct'),
]
