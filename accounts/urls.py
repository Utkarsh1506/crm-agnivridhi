from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password-change/', views.change_password, name='change_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/superuser/', views.superuser_dashboard, name='superuser_dashboard'),
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
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
    
    # PDF Downloads
    path('pdf/payment/<int:payment_id>/', views.download_payment_receipt_pdf, name='download_payment_receipt'),
    path('pdf/booking/<int:booking_id>/', views.download_booking_confirmation_pdf, name='download_booking_confirmation'),
    path('pdf/application/<int:application_id>/', views.download_application_form_pdf, name='download_application_form'),
]
