from django import forms
from .models import Agreement
from clients.models import Client
from employees.models import Employee
from datetime import date
from decimal import Decimal


class AgreementForm(forms.ModelForm):
    """Form for creating and editing agreements"""
    
    # Override fields for better widgets and validation
    service_receiver_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter service receiver name'
        }),
        label='Service Receiver Name'
    )
    
    service_receiver_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter complete address'
        }),
        label='Address'
    )
    
    date_of_agreement = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        initial=date.today,
        label='Date of Agreement'
    )
    
    service_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe the service in detail'
        }),
        label='Service Description'
    )
    
    total_amount_pitched = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01'
        }),
        label='Total Amount Pitched'
    )
    
    received_amount_stage1 = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00 (without GST)',
            'step': '0.01'
        }),
        label='Received Amount (Stage 1) - Without GST'
    )
    
    pending_amount_stage2 = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00 (optional)',
            'step': '0.01'
        }),
        label='Pending Amount (Stage 2) - Optional',
        help_text='Leave blank or 0 if no pending amount'
    )
    
    commission_percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0',
            'max': '100'
        }),
        label='Commission Percentage (%)',
        help_text='Commission percentage after disbursement'
    )
    
    client = forms.ModelChoiceField(
        queryset=Client.objects.filter(is_approved=True),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Client (Optional)',
        help_text='Select client if applicable'
    )
    
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(status='ACTIVE'),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Employee (Optional)',
        help_text='Select employee handling this agreement'
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Additional notes (optional)'
        }),
        label='Notes'
    )
    
    class Meta:
        model = Agreement
        fields = [
            'agreement_type',
            'service_receiver_name',
            'service_receiver_address',
            'date_of_agreement',
            'service_description',
            'total_amount_pitched',
            'received_amount_stage1',
            'pending_amount_stage2',
            'commission_percentage',
            'commission_stage',
            'client',
            'employee',
            'notes'
        ]
        widgets = {
            'agreement_type': forms.Select(attrs={'class': 'form-control'}),
            'commission_stage': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        total_amount = cleaned_data.get('total_amount_pitched')
        received_amount = cleaned_data.get('received_amount_stage1')
        pending_amount = cleaned_data.get('pending_amount_stage2')
        
        # Validate amounts
        if total_amount and received_amount:
            if received_amount > total_amount:
                raise forms.ValidationError(
                    'Received amount cannot be greater than total amount pitched.'
                )
        
        # Set pending amount to 0 if None
        if not pending_amount:
            cleaned_data['pending_amount_stage2'] = Decimal('0.00')
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter clients based on user role
        if user:
            if hasattr(user, 'role'):
                if user.role in ['sales', 'employee']:
                    self.fields['client'].queryset = Client.objects.filter(
                        assigned_sales=user,
                        is_approved=True
                    )
