from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    # Client creation
    path('create/', views.create_client, name='create_client'),
    
    # Client profile completion (for clients to fill details after creation)
    path('complete-profile/', views.complete_client_profile, name='complete_profile'),
    
    # Client detail
    path('<int:pk>/', views.client_detail, name='client_detail'),
    
    # Approval workflow
    path('pending-approval/', views.pending_approval_clients, name='pending_approval_clients'),
    path('<int:pk>/approve/', views.approve_client, name='approve_client'),
    
    # Lists
    path('my-clients/', views.sales_clients_list, name='sales_clients_list'),
    path('team-clients/', views.manager_clients_list, name='manager_clients_list'),
    path('admin/', views.admin_clients_list, name='admin_clients_list'),
]
