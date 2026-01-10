from django.urls import path
from . import views

# -----------------------------------------------------------------------------
# Django app namespace (prep for namespaced includes)
app_name = 'accounts'

# -----------------------------------------------------------------------------
# Dashboard routing (role-specific)
#
# Routes provide a single predictable location per role:
#  - /dashboard/                 -> redirects to role-appropriate dashboard
#  - /dashboard/client/          -> client portal
#  - /dashboard/sales/           -> sales dashboard
#  - /dashboard/manager/         -> manager dashboard
#  - /dashboard/admin/           -> admin dashboard (for ADMIN role users)
#  - /dashboard/owner/           -> owner/dashboard for Admins flagged is_owner
#
# Keep the generic `application_list` and other deprecated generic endpoints
# as redirectors to role-specific pages to maintain privacy and a clear URL map.
# -----------------------------------------------------------------------------

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password-change/', views.change_password, name='change_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/superuser/', views.superuser_dashboard, name='superuser_dashboard'),
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),
    path('dashboard/owner/mark-credential-sent/<int:credential_id>/', views.mark_credential_as_sent, name='mark_credential_as_sent'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    path('users/', views.users_list, name='users_list'),
    path('pending-approvals/', views.pending_approvals, name='pending_approvals'),
    path('team/members/', views.team_members_list, name='team_members_list'),
    path('team/clients/', views.team_clients_list, name='team_clients_list'),
    path('team/diagnostic/', views.team_diagnostic, name='team_diagnostic'),
    path('dashboard/sales/', views.sales_dashboard, name='sales_dashboard'),
    path('bookings/<int:booking_id>/record-payment/', views.record_payment, name='record_payment'),
    path('payments/<int:payment_id>/approve/', views.approve_payment, name='approve_payment'),
    path('payments/<int:payment_id>/reject/', views.reject_payment, name='reject_payment'),
    path('dashboard/client/', views.client_portal, name='client_portal'),
    
    # Export URLs
    path('export/clients/', views.export_clients, name='export_clients'),
    path('export/bookings/', views.export_bookings, name='export_bookings'),
    path('export/payments/', views.export_payments, name='export_payments'),
    path('export/dashboard/', views.export_dashboard_data, name='export_dashboard_data'),
    
    # Search
    path('search/', views.global_search, name='global_search'),
    
    # Reports
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('revenue/report/', views.revenue_report, name='revenue_report'),
    path('revenue/report/export-excel/', views.revenue_report_excel, name='revenue_report_excel'),

    # Route Directory (staff-only)
    path('routes/', views.route_directory, name='route_directory'),
    
    # PDF Downloads
    path('pdf/payment/<int:payment_id>/', views.download_payment_receipt_pdf, name='download_payment_receipt'),
    path('pdf/booking/<int:booking_id>/', views.download_booking_confirmation_pdf, name='download_booking_confirmation'),
    path('pdf/application/<int:application_id>/', views.download_application_form_pdf, name='download_application_form'),
]
