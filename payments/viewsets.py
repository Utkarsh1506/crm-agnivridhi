"""
API ViewSets for Payments app
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import PaymentSerializer, PaymentListSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Payment CRUD operations
    
    Permissions:
    - List/Retrieve: All authenticated users
    - Create: Staff users only
    - Update/Delete: Admin users only
    """
    queryset = Payment.objects.select_related('client', 'booking', 'received_by', 'created_by').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'payment_date']
    search_fields = ['client__company_name', 'transaction_id', 'reference_id']
    ordering_fields = ['created_at', 'payment_date', 'amount']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return PaymentListSerializer
        return PaymentSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Salespersons see only payments for their clients
        if not user.is_staff and hasattr(user, 'role') and user.role == 'SALESPERSON':
            queryset = queryset.filter(client__salesperson=user)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set created_by on creation"""
        if not self.request.user.is_staff:
            return Response(
                {'detail': 'Only staff can create payments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        """Only admins can update payments"""
        if not self.request.user.is_superuser:
            return Response(
                {'detail': 'Only admins can update payments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        """Only admins can delete payments"""
        if not request.user.is_superuser:
            return Response(
                {'detail': 'Only admins can delete payments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve payment"""
        if not request.user.is_staff:
            return Response(
                {'detail': 'Only staff can approve payments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        payment = self.get_object()
        
        if payment.status == 'APPROVED':
            return Response(
                {'detail': 'Payment is already approved.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.status = 'APPROVED'
        payment.save()
        
        # Log activity
        from activity_logs.models import ActivityLog
        ActivityLog.log_action(
            request=request,
            user=request.user,
            action='APPROVE',
            entity_type='PAYMENT',
            entity_id=payment.id,
            description=f'Approved payment of ₹{payment.amount} for {payment.client.company_name}'
        )
        
        # Send email notification
        try:
            from accounts.email_utils import send_payment_approval_email
            send_payment_approval_email(payment, request.user)
        except Exception as e:
            print(f"Error sending approval email: {e}")
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject payment"""
        if not request.user.is_staff:
            return Response(
                {'detail': 'Only staff can reject payments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        payment = self.get_object()
        reason = request.data.get('reason', 'No reason provided')
        
        if payment.status == 'REJECTED':
            return Response(
                {'detail': 'Payment is already rejected.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.status = 'REJECTED'
        payment.notes = f"Rejected: {reason}" if not payment.notes else f"{payment.notes}\nRejected: {reason}"
        payment.save()
        
        # Log activity
        from activity_logs.models import ActivityLog
        ActivityLog.log_action(
            request=request,
            user=request.user,
            action='REJECT',
            entity_type='PAYMENT',
            entity_id=payment.id,
            description=f'Rejected payment of ₹{payment.amount} for {payment.client.company_name}. Reason: {reason}'
        )
        
        # Send email notification
        try:
            from accounts.email_utils import send_payment_rejection_email
            send_payment_rejection_email(payment, request.user)
        except Exception as e:
            print(f"Error sending rejection email: {e}")
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)
