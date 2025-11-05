"""
Serializers for Bookings app
"""
from rest_framework import serializers
from .models import Booking, Service


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service model"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'category', 'category_display', 'description', 'base_price', 'is_active']


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    client_name = serializers.CharField(source='client.company_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    salesperson_name = serializers.CharField(source='salesperson.get_full_name', read_only=True, allow_null=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'client', 'client_name', 'service', 'service_name',
            'booking_date', 'amount', 'status', 'status_display',
            'salesperson', 'salesperson_name', 'notes',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def validate_amount(self, value):
        """Validate amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class BookingListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing bookings"""
    client_name = serializers.CharField(source='client.company_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'client', 'client_name', 'service', 'service_name',
            'booking_date', 'amount', 'status', 'status_display', 'created_at'
        ]
