from django.urls import path
from . import views

# Namespace for reverse() calls like 'payments:payment_detail'
app_name = 'payments'

urlpatterns = [
    # Role-specific payment pages
    path('', views.payment_list, name='payment_list'),  # deprecated generic -> redirects
    path('client/', views.client_payments_list, name='client_payments_list'),
    path('sales/', views.sales_payments_list, name='sales_payments_list'),
    path('team/', views.team_payments_list, name='team_payments_list'),

    # Detail
    path('<int:pk>/', views.payment_detail, name='payment_detail'),
    
    # Payment actions
    path('record/<int:booking_id>/', views.record_payment, name='record_payment'),
    path('approve/<int:payment_id>/', views.approve_payment, name='approve_payment'),
    path('reject/<int:payment_id>/', views.reject_payment, name='reject_payment'),
]
