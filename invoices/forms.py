from django import forms
from .models import Invoice
from clients.models import Client
from datetime import date
import random


def generate_hsn_code():
    """Generate unique HSN/SAC code for services"""
    # SAC codes for professional services typically start with 998
    # Generate random 6-digit code: 998XXX
    return f"998{random.randint(100, 999)}"


class InvoiceForm(forms.ModelForm):
    # Make client optional for proforma
    client_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter client/company name (for Proforma)'
        }),
        label='Client Name (Manual Entry)'
    )
    client_contact_person = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contact person name'
        }),
        label='Contact Person'
    )

    client_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Full address'
        }),
        label='Address'
    )

    client_city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        }),
        label='City'
    )

    client_state = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'State'
        }),
        label='State'
    )

    client_pincode = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pincode'
        }),
        label='Pincode'
    )

    client_gstin = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'GSTIN (optional)'
        }),
        label='GSTIN'
    )

    client_mobile = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mobile/Phone'
        }),
        label='Mobile/Phone'
    )

    class Meta:
        model = Invoice
        fields = [
            'invoice_type', 'client', 'issue_date', 'due_date',
            'item_description', 'hsn_sac', 'quantity', 'rate', 
            'gst_rate', 'place_of_supply', 'notes',
            # Manual client details for Proforma
            'client_name', 'client_contact_person', 'client_address',
            'client_city', 'client_state', 'client_pincode',
            'client_gstin', 'client_mobile'
        ]
        widgets = {
            'invoice_type': forms.Select(attrs={'class': 'form-select'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'item_description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Enter detailed description of services/products...'
            }),
            'hsn_sac': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '998314'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '1'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '10000'}),
            'gst_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '18'}),
            'place_of_supply': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Maharashtra'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Payment terms...'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Make client field optional initially
        self.fields['client'].required = False
        
        # Set default issue date and auto-generate HSN
        if not self.instance.pk:
            self.initial['issue_date'] = date.today()
            self.initial['quantity'] = 1
            self.initial['gst_rate'] = 18
            self.initial['place_of_supply'] = 'Uttar Pradesh'
            self.initial['hsn_sac'] = generate_hsn_code()  # Auto-generate unique HSN
        
        # Filter clients by user role
        if user:
            role = getattr(user, 'role', '').upper()
            if role in ['ADMIN', 'OWNER'] or user.is_superuser:
                self.fields['client'].queryset = Client.objects.filter(is_approved=True)
            elif role == 'MANAGER':
                from django.db import models as django_models
                self.fields['client'].queryset = Client.objects.filter(
                    django_models.Q(assigned_sales__manager=user) |
                    django_models.Q(assigned_manager=user) |
                    django_models.Q(created_by=user),
                    is_approved=True
                ).distinct()
            else:  # Sales
                from django.db import models as django_models
                self.fields['client'].queryset = Client.objects.filter(
                    django_models.Q(assigned_sales=user) | django_models.Q(created_by=user),
                    is_approved=True
                ).distinct()
    
    def clean(self):
        cleaned_data = super().clean()
        invoice_type = cleaned_data.get('invoice_type')
        client = cleaned_data.get('client')
        client_name = cleaned_data.get('client_name')
        client_address = cleaned_data.get('client_address')
        client_city = cleaned_data.get('client_city')
        client_state = cleaned_data.get('client_state')
        client_pincode = cleaned_data.get('client_pincode')
        client_mobile = cleaned_data.get('client_mobile')
        
        # Both Tax Invoice and Proforma can use existing client OR manual entry
        # Tax Invoice: allow manual entry if no client selected
        if invoice_type == 'tax' and not client:
            # Only client name is required for manual entry
            if not client_name:
                self.add_error('client_name', 'Client name is required when no existing client is selected.')
        
        # Proforma: either existing client OR manual client name (other fields optional)
        if invoice_type == 'proforma' and not client:
            # Only client name is required for manual entry
            if not client_name:
                self.add_error('client_name', 'Client name is required for Proforma when no existing client is selected.')
        
        return cleaned_data
