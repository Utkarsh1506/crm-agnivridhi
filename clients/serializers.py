"""
Serializers for Clients app
"""
from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model"""
    sector_display = serializers.CharField(source='get_sector_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    salesperson_name = serializers.CharField(source='salesperson.get_full_name', read_only=True, allow_null=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Client
        fields = [
            'id', 'company_name', 'contact_name', 'contact_email', 'contact_phone',
            'pan_number', 'gst_number', 'address', 'city', 'state', 'pincode',
            'sector', 'sector_display', 'status', 'status_display',
            'salesperson', 'salesperson_name', 'notes',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def validate_contact_email(self, value):
        """Validate email uniqueness"""
        if value:
            client_id = self.instance.id if self.instance else None
            if Client.objects.filter(contact_email=value).exclude(id=client_id).exists():
                raise serializers.ValidationError("A client with this email already exists.")
        return value
    
    def validate_pan_number(self, value):
        """Validate PAN format"""
        if value and len(value) != 10:
            raise serializers.ValidationError("PAN number must be 10 characters.")
        return value.upper() if value else value


class ClientListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing clients"""
    sector_display = serializers.CharField(source='get_sector_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    salesperson_name = serializers.CharField(source='salesperson.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Client
        fields = [
            'id', 'company_name', 'contact_name', 'contact_email', 'contact_phone',
            'sector', 'sector_display', 'status', 'status_display',
            'salesperson', 'salesperson_name', 'created_at'
        ]
