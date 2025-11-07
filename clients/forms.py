from django import forms
from django.contrib.auth import get_user_model
from .models import Client

User = get_user_model()


class ClientCreationForm(forms.ModelForm):
    """Form for creating a new client"""
    
    # User fields (for the User account)
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@company.com'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 9876543210'})
    )
    
    class Meta:
        model = Client
        fields = [
            'company_name', 'business_type', 'sector', 'company_age',
            'registration_number', 'gst_number', 'pan_number',
            'address_line1', 'address_line2', 'city', 'state', 'pincode',
            'annual_turnover', 'funding_required', 'existing_loans',
            'contact_person', 'contact_email', 'contact_phone', 'alternate_phone',
            'business_description', 'funding_purpose'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ABC Pvt Ltd'}),
            'business_type': forms.Select(attrs={'class': 'form-select'}),
            'sector': forms.Select(attrs={'class': 'form-select'}),
            'company_age': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'U12345AB2020PTC123456'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '22AAAAA0000A1Z5'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ABCDE1234F'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '400001'}),
            'annual_turnover': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'funding_required': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'existing_loans': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'alternate_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'business_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'funding_purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.created_by = kwargs.pop('created_by', None)
        super().__init__(*args, **kwargs)
        
        # Make some fields optional
        optional_fields = ['registration_number', 'gst_number', 'pan_number', 
                          'address_line2', 'existing_loans', 'alternate_phone',
                          'business_description', 'funding_purpose']
        for field in optional_fields:
            self.fields[field].required = False
    
    def save(self, commit=True):
        """Create client profile"""
        client = super().save(commit=False)
        
        # Create user account for the client
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Generate a unique username from email
        email = self.cleaned_data.get('email')
        username = email.split('@')[0]
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{email.split('@')[0]}{counter}"
            counter += 1
        
        # Create user account with data from form fields
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            phone=self.cleaned_data.get('phone'),
            role='CLIENT',
            password=User.objects.make_random_password(12)  # Random password, will be sent via email
        )
        
        client.user = user
        client.created_by = self.created_by
        
        # Set approval based on creator role
        if self.created_by and self.created_by.role in ['ADMIN', 'MANAGER', 'OWNER']:
            # Admins and managers can directly create approved clients
            client.is_approved = True
            client.approved_by = self.created_by
            from django.utils import timezone
            client.approved_at = timezone.now()
        else:
            # Sales need manager approval
            client.is_approved = False
            if self.created_by and hasattr(self.created_by, 'manager'):
                client.assigned_manager = self.created_by.manager
        
        # Set assigned sales
        if self.created_by and self.created_by.role == 'SALES':
            client.assigned_sales = self.created_by
        
        if commit:
            client.save()
        
        return client


class ClientApprovalForm(forms.Form):
    """Form for approving/rejecting a client"""
    
    action = forms.ChoiceField(
        choices=[('approve', 'Approve'), ('reject', 'Reject')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    rejection_reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Reason for rejection (required if rejecting)'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        rejection_reason = cleaned_data.get('rejection_reason')
        
        if action == 'reject' and not rejection_reason:
            raise forms.ValidationError('Rejection reason is required when rejecting a client.')
        
        return cleaned_data
