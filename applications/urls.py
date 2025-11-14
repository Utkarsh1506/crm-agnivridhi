from django.urls import path
from . import views

# Namespace for reverse() calls like 'applications:manager_application_detail'
app_name = 'applications'

urlpatterns = [
    # Role-specific application pages
    path('', views.application_list, name='application_list'),  # deprecated generic -> redirects
    path('client/', views.client_applications_list, name='client_applications_list'),
    path('sales/', views.sales_applications_list, name='sales_applications_list'),
    path('team/', views.team_applications_list, name='team_applications_list'),
    path('pending/', views.pending_applications, name='pending_applications'),

    # Actions and detail
    path('create-from-booking/<int:booking_id>/', views.create_application_from_booking, name='create_application_from_booking'),
    path('<int:pk>/', views.application_detail, name='application_detail'),  # deprecated generic -> redirects
    
    # Role-specific detail views
    path('client/<int:pk>/', views.client_application_detail, name='client_application_detail'),
    path('sales/<int:pk>/', views.sales_application_detail, name='sales_application_detail'),
    path('manager/<int:pk>/', views.manager_application_detail, name='manager_application_detail'),
    path('owner/<int:pk>/', views.owner_application_detail, name='owner_application_detail'),
    # Admin-friendly alias for clarity (same as owner view for ADMIN role users)
    path('admin/<int:pk>/', views.owner_application_detail, name='admin_application_detail'),
    
    path('create/<int:scheme_id>/', views.create_application, name='create_application'),
    
    # Manager actions
    path('<int:pk>/approve/', views.approve_application, name='approve_application'),
    path('<int:pk>/reject/', views.reject_application, name='reject_application'),
    path('<int:pk>/update-status/', views.update_application_status, name='update_application_status'),
]
