"""
Employee module URL configuration.
Handles all employee management and verification routes.
"""
from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    # ====================================================================
    # ADMIN/HR MANAGEMENT ROUTES (Login Required)
    # ====================================================================
    
    # List and create employees
    path(
        'list/',
        views.employee_list_view,
        name='employee_list'
    ),
    path(
        'create/',
        views.employee_create_view,
        name='employee_create'
    ),
    
    # View, edit, manage specific employee
    path(
        '<int:pk>/',
        views.employee_detail_view,
        name='employee_detail'
    ),
    path(
        '<int:pk>/status-toggle/',
        views.employee_status_toggle_view,
        name='employee_status_toggle'
    ),
    path(
        '<int:pk>/download-id-card/',
        views.employee_download_id_card_view,
        name='employee_download_id_card'
    ),
    
    # Verification logs (audit trail)
    path(
        '<int:pk>/verification-logs/',
        views.employee_verification_logs_view,
        name='employee_verification_logs'
    ),
    
    # ====================================================================
    # PUBLIC VERIFICATION ROUTE (No Login Required, Rate Limited)
    # ====================================================================
    path(
        'verify/<str:employee_id>/',
        views.employee_verify_public_view,
        name='employee_verify_public'
    ),
]
