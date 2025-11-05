"""
API ViewSets for Applications app
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Application
from .serializers import ApplicationSerializer, ApplicationListSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Application CRUD operations
    
    Permissions:
    - List/Retrieve: All authenticated users
    - Create/Update: Staff users only
    - Delete: Admin users only
    """
    queryset = Application.objects.select_related('client', 'scheme', 'assigned_to', 'created_by').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'scheme', 'assigned_to']
    search_fields = ['client__company_name', 'scheme__name']
    ordering_fields = ['created_at', 'application_date', 'amount_requested']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return ApplicationListSerializer
        return ApplicationSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Users see only applications assigned to them or their clients
        if not user.is_staff:
            queryset = queryset.filter(assigned_to=user) | queryset.filter(client__salesperson=user)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set created_by on creation"""
        if not self.request.user.is_staff:
            return Response(
                {'detail': 'Only staff can create applications.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        """Only staff can update applications"""
        if not self.request.user.is_staff:
            return Response(
                {'detail': 'Only staff can update applications.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        """Only admins can delete applications"""
        if not request.user.is_superuser:
            return Response(
                {'detail': 'Only admins can delete applications.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update application status"""
        if not request.user.is_staff:
            return Response(
                {'detail': 'Only staff can update application status.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        application = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'detail': 'Status is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_status = application.status
        application.status = new_status
        
        # Update approved amount if status is approved
        if new_status == 'APPROVED' and 'amount_approved' in request.data:
            application.amount_approved = request.data['amount_approved']
        
        # Update rejection reason if status is rejected
        if new_status == 'REJECTED' and 'rejection_reason' in request.data:
            application.rejection_reason = request.data['rejection_reason']
        
        application.save()
        
        # Log activity
        from activity_logs.models import ActivityLog
        ActivityLog.log_action(
            request=request,
            user=request.user,
            action='STATUS_CHANGE',
            entity_type='APPLICATION',
            entity_id=application.id,
            description=f'Changed application status from {old_status} to {new_status}',
            old_value=old_status,
            new_value=new_status
        )
        
        # Send email notification
        try:
            from accounts.email_utils import send_application_status_email
            send_application_status_email(application)
        except Exception as e:
            print(f"Error sending status email: {e}")
        
        serializer = self.get_serializer(application)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Assign application to user"""
        if not request.user.is_staff:
            return Response(
                {'detail': 'Only staff can assign applications.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        application = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'detail': 'user_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from accounts.models import User
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        old_assigned = application.assigned_to
        application.assigned_to = user
        application.save()
        
        # Log activity
        from activity_logs.models import ActivityLog
        ActivityLog.log_action(
            request=request,
            user=request.user,
            action='ASSIGN',
            entity_type='APPLICATION',
            entity_id=application.id,
            description=f'Assigned application to {user.get_full_name()}',
            old_value=old_assigned.get_full_name() if old_assigned else None,
            new_value=user.get_full_name()
        )
        
        serializer = self.get_serializer(application)
        return Response(serializer.data)
