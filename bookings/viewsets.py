"""
API ViewSets for Bookings app
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Booking, Service
from .serializers import BookingSerializer, BookingListSerializer, ServiceSerializer


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Service (Read-only)
    Only staff can manage services via admin panel
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'base_price']
    ordering = ['name']


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Booking CRUD operations
    
    Permissions:
    - List/Retrieve: All authenticated users
    - Create/Update: Staff users only
    - Delete: Admin users only
    """
    queryset = Booking.objects.select_related('client', 'service', 'salesperson', 'created_by').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'salesperson', 'booking_date']
    search_fields = ['client__company_name', 'service__name']
    ordering_fields = ['created_at', 'booking_date', 'amount']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return BookingListSerializer
        return BookingSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Salespersons see only their bookings
        if not user.is_staff and hasattr(user, 'role') and user.role == 'SALESPERSON':
            queryset = queryset.filter(salesperson=user)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set created_by on creation"""
        if not self.request.user.is_staff:
            return Response(
                {'detail': 'Only staff can create bookings.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        """Only staff can update bookings"""
        if not self.request.user.is_staff:
            return Response(
                {'detail': 'Only staff can update bookings.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        """Only admins can delete bookings"""
        if not request.user.is_staff:
            return Response(
                {'detail': 'You do not have permission to delete bookings.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update booking status"""
        if not request.user.is_staff:
            return Response(
                {'detail': 'Only staff can update booking status.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        booking = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'detail': 'Status is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_status = booking.status
        booking.status = new_status
        booking.save()
        
        # Log activity
        from activity_logs.models import ActivityLog
        ActivityLog.log_action(
            request=request,
            user=request.user,
            action='STATUS_CHANGE',
            entity_type='BOOKING',
            entity_id=booking.id,
            description=f'Changed booking status from {old_status} to {new_status}',
            old_value=old_status,
            new_value=new_status
        )
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
