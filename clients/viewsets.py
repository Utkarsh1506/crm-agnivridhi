"""
API ViewSets for Clients app
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client
from .serializers import ClientSerializer, ClientListSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Client CRUD operations
    
    Permissions:
    - List/Retrieve: All authenticated users
    - Create/Update/Delete: Staff users only
    """
    queryset = Client.objects.select_related('salesperson', 'created_by').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sector', 'status', 'salesperson']
    search_fields = ['company_name', 'contact_name', 'contact_email', 'contact_phone', 'pan_number', 'gst_number']
    ordering_fields = ['created_at', 'updated_at', 'company_name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return ClientListSerializer
        return ClientSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Salespersons see only their clients
        if not user.is_staff and hasattr(user, 'role') and user.role == 'SALESPERSON':
            queryset = queryset.filter(salesperson=user)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set created_by on creation"""
        serializer.save(created_by=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Only admins can delete clients"""
        if not request.user.is_staff:
            return Response(
                {'detail': 'You do not have permission to delete clients.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Get all bookings for a client"""
        client = self.get_object()
        bookings = client.booking_set.all()
        from bookings.serializers import BookingListSerializer
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        """Get all payments for a client"""
        client = self.get_object()
        payments = client.payment_set.all()
        from payments.serializers import PaymentListSerializer
        serializer = PaymentListSerializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """Get all applications for a client"""
        client = self.get_object()
        applications = client.application_set.all()
        from applications.serializers import ApplicationListSerializer
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)
