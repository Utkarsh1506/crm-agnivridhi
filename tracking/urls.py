from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    # Client views
    path('dashboard/', views.client_dashboard, name='client_dashboard'),
    path('timeline/', views.client_timeline, name='client_timeline'),
    path('services/', views.client_services, name='client_services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    
    # Sales views
    path('sales/client/<int:client_id>/activities/', views.sales_client_activities, name='sales_client_activities'),
    path('sales/client/<int:client_id>/add-activity/', views.sales_add_activity, name='sales_add_activity'),
    path('sales/activity/<int:activity_id>/edit/', views.sales_edit_activity, name='sales_edit_activity'),
    path('sales/activity/<int:activity_id>/delete/', views.sales_delete_activity, name='sales_delete_activity'),
]
