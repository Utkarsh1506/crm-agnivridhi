from django.urls import path
from . import views

urlpatterns = [
    path('sales/', views.sales_invoice_list, name='sales_invoice_list'),
    path('sales/create/', views.sales_invoice_create, name='sales_invoice_create'),
    path('sales/<int:pk>/pdf/', views.sales_invoice_pdf, name='sales_invoice_pdf'),
]
