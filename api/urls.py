"""
API URLs for Agnivridhi CRM
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clients.viewsets import ClientViewSet
from bookings.viewsets import BookingViewSet, ServiceViewSet
from payments.viewsets import PaymentViewSet
from applications.viewsets import ApplicationViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]
