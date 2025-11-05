"""
Serializers for Applications app
"""
from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Application model"""
    client_name = serializers.CharField(source='client.company_name', read_only=True)
    scheme_name = serializers.CharField(source='scheme.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True, allow_null=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'client', 'client_name', 'scheme', 'scheme_name',
            'application_date', 'amount_requested', 'amount_approved',
            'status', 'status_display', 'assigned_to', 'assigned_to_name',
            'notes', 'rejection_reason',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def validate_amount_requested(self, value):
        """Validate amount is positive"""
        if value and value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        if data.get('amount_approved') and data.get('amount_requested'):
            if data['amount_approved'] > data['amount_requested']:
                raise serializers.ValidationError({
                    'amount_approved': "Approved amount cannot exceed requested amount."
                })
        return data


class ApplicationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing applications"""
    client_name = serializers.CharField(source='client.company_name', read_only=True)
    scheme_name = serializers.CharField(source='scheme.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'client', 'client_name', 'scheme', 'scheme_name',
            'application_date', 'amount_requested', 'amount_approved',
            'status', 'status_display', 'created_at'
        ]
