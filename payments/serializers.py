"""
Serializers for Payments app
"""
from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""
    client_name = serializers.CharField(source='client.company_name', read_only=True)
    booking_id = serializers.CharField(source='booking.id', read_only=True, allow_null=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    received_by_name = serializers.CharField(source='received_by.get_full_name', read_only=True, allow_null=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'client', 'client_name', 'booking', 'booking_id',
            'amount', 'payment_method', 'payment_method_display',
            'transaction_id', 'reference_id', 'payment_date',
            'status', 'status_display', 'received_by', 'received_by_name',
            'proof', 'notes', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def validate_amount(self, value):
        """Validate amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class PaymentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing payments"""
    client_name = serializers.CharField(source='client.company_name', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'client', 'client_name', 'amount',
            'payment_method', 'payment_method_display',
            'payment_date', 'status', 'status_display',
            'reference_id', 'created_at'
        ]
