from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    # Sales URLs
    path('sales/', views.sales_invoice_list, name='sales_invoice_list'),
    path('sales/create/', views.sales_invoice_create, name='sales_invoice_create'),
    path('sales/<int:pk>/pdf/', views.sales_invoice_pdf, name='sales_invoice_pdf'),
    
    # Manager URLs
    path('manager/', views.manager_invoice_list, name='manager_invoice_list'),
    path('manager/create/', views.manager_invoice_create, name='manager_invoice_create'),
    path('manager/<int:pk>/pdf/', views.manager_invoice_pdf, name='manager_invoice_pdf'),
    
    # Admin/Owner URLs
    path('admin/', views.admin_invoice_list, name='admin_invoice_list'),
    path('admin/create/', views.admin_invoice_create, name='admin_invoice_create'),
    path('admin/<int:pk>/pdf/', views.admin_invoice_pdf, name='admin_invoice_pdf'),
]
