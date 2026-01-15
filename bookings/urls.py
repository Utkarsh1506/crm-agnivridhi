from django.urls import path
from . import views

# Namespace for reverse() calls like 'bookings:booking_detail'
app_name = 'bookings'

urlpatterns = [
    # Role-specific booking pages
    path('', views.booking_list, name='booking_list'),  # deprecated generic -> redirects
    path('client/', views.client_bookings_list, name='client_bookings_list'),
    path('sales/', views.sales_bookings_list, name='sales_bookings_list'),
    path('team/', views.team_bookings_list, name='team_bookings_list'),

    # Actions
    path('create/scheme/<int:scheme_id>/', views.create_scheme_documentation_booking, name='create_documentation_booking'),
    path('create/client/<int:client_id>/', views.create_booking_for_client, name='create_booking_for_client'),

    # Detail
    path('<int:id>/', views.booking_detail, name='booking_detail'),
    path('<int:booking_id>/documents/', views.collect_documents, name='collect_documents'),
