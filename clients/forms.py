from django import forms
from django.contrib.auth import get_user_model
from .models import Client
from django.utils import timezone

User = get_user_model()


class QuickClientCreationForm(forms.Form):
    """
    Simplified form for quick client creation.
    Only requires: company name, contact person, email, phone.
    Client fills remaining details after login.
    """
    company_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ABC Pvt Ltd'
        }),
        help_text='Company or business name'
    )
    
    contact_person = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'John Doe'
        }),
        help_text='Primary contact person name'
    )
    
    contact_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'john@company.com'
        }),
        help_text='Primary contact email (will be used for login)'
    )
    
    contact_phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+91 9876543210'
        }),
        help_text='Primary contact phone'
    )
    
    initial_service = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Company Registration, GST Registration, etc.'
        }),
        help_text='Enter the service client is interested in (optional)'
    )
    
    assigned_manager = forms.ModelChoiceField(
        queryset=User.objects.none(),  # Will be set in __init__
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text='Select manager to assign this client (optional for sales)'
    )

    # Revenue fields
    total_pitched_amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        help_text='Total pitched amount (₹) excluding GST'
    )
    gst_percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        min_value=0,
        initial=18.00,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '18.00'}),
        help_text='GST % (default 18%)'
    )
    received_amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        help_text='Amount received (₹) so far'
    )
    pending_amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00', 'readonly': 'readonly'}),
        help_text='Pending amount (₹) - auto-calculated'
    )
    
    def __init__(self, *args, **kwargs):
        self.created_by = kwargs.pop('created_by', None)
        super().__init__(*args, **kwargs)
        
        # Setup manager choices based on user role
        if self.created_by:
            if self.created_by.role == 'SALES':
                # Sales can select from available managers
                # Prioritize their own manager first
                self.fields['assigned_manager'].queryset = User.objects.filter(
                    role__in=['MANAGER', 'ADMIN']
                ).order_by('first_name', 'last_name')
                
                # Set default to sales person's manager if available
                if hasattr(self.created_by, 'manager') and self.created_by.manager:
                    self.fields['assigned_manager'].initial = self.created_by.manager
                    self.fields['assigned_manager'].help_text = f'Default: Your manager ({self.created_by.manager.get_full_name()})'
            elif self.created_by.role in ['ADMIN', 'OWNER']:
                # Admin/Owner can see all managers
                self.fields['assigned_manager'].queryset = User.objects.filter(
                    role='MANAGER'
                ).order_by('first_name', 'last_name')
            else:
                # Manager creating client - no need to show this field
                self.fields['assigned_manager'].widget = forms.HiddenInput()
    
    def clean_contact_email(self):
        """Check if email already exists"""
        email = self.cleaned_data.get('contact_email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email
    
    def save(self):
        """Create minimal client profile with user account"""
        # Generate username from email
        email = self.cleaned_data.get('contact_email')
        username = email.split('@')[0]
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{email.split('@')[0]}{counter}"
            counter += 1
        
        # Create user account
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=self.cleaned_data.get('contact_person').split()[0],
            last_name=' '.join(self.cleaned_data.get('contact_person').split()[1:]) if len(self.cleaned_data.get('contact_person').split()) > 1 else '',
            phone=self.cleaned_data.get('contact_phone'),
            role='CLIENT',
            password=User.objects.make_random_password(12)
        )
        
        # Create minimal client profile
        from decimal import Decimal
        total_pitched = Decimal(self.cleaned_data.get('total_pitched_amount') or 0)
        received = Decimal(self.cleaned_data.get('received_amount') or 0)
        gst_pct = Decimal(self.cleaned_data.get('gst_percentage') or 18)
        
        # Calculate GST
        gst_amount = (total_pitched * gst_pct / Decimal('100')).quantize(Decimal('0.01'))
        total_with_gst = total_pitched + gst_amount
        
        # Normalize amounts
        if received > total_with_gst:
            total_with_gst = received
            gst_amount = Decimal('0.00')
        
        pending = total_with_gst - received
        if pending < 0:
            pending = Decimal('0.00')

        client = Client.objects.create(
            user=user,
            company_name=self.cleaned_data.get('company_name'),
            contact_person=self.cleaned_data.get('contact_person'),
            contact_email=email,
            contact_phone=self.cleaned_data.get('contact_phone'),
            created_by=self.created_by,
            status='PENDING_DOCS',  # Client needs to complete profile
            is_approved=True if self.created_by and self.created_by.role in ['ADMIN', 'MANAGER', 'OWNER'] else False,
            total_pitched_amount=total_pitched,
            gst_percentage=gst_pct,
            gst_amount=gst_amount,
            total_with_gst=total_with_gst,
            received_amount=received,
            pending_amount=pending
        )
        
        # Set assigned sales and manager
        if self.created_by and self.created_by.role == 'SALES':
            client.assigned_sales = self.created_by
            
            # Use selected manager or fall back to sales person's default manager
            selected_manager = self.cleaned_data.get('assigned_manager')
            if selected_manager:
                client.assigned_manager = selected_manager
            elif hasattr(self.created_by, 'manager') and self.created_by.manager:
                client.assigned_manager = self.created_by.manager
        elif self.created_by and self.created_by.role == 'MANAGER':
            # Manager creating client - assign to themselves
            client.assigned_manager = self.created_by
        elif self.created_by and self.created_by.role in ['ADMIN', 'OWNER']:
            # Admin/Owner can optionally assign manager
            selected_manager = self.cleaned_data.get('assigned_manager')
            if selected_manager:
                client.assigned_manager = selected_manager
        
        # Auto-approve if created by admin/manager/owner
        if self.created_by and self.created_by.role in ['ADMIN', 'MANAGER', 'OWNER']:
            client.approved_by = self.created_by
            client.approved_at = timezone.now()
        
        client.save()

        # Create initial revenue log entry
        try:
            from payments.models import RevenueEntry
            RevenueEntry.objects.create(
                client=client,
                recorded_by=self.created_by,
                total_pitched_amount=client.total_pitched_amount,
                received_amount=client.received_amount,
                pending_amount=client.pending_amount,
                source='CLIENT_CREATION',
                note='Initial revenue captured during client creation'
            )
        except Exception:
            # Avoid breaking flow if revenue logging fails
            pass
        
        # Create initial service booking if provided
        initial_service_text = self.cleaned_data.get('initial_service')
        if initial_service_text and initial_service_text.strip():
            from bookings.models import Booking, Service
            from datetime import timedelta
            
            # Get or create a default "Consultation" service for initial bookings
            consultation_service, created = Service.objects.get_or_create(
                name='Initial Consultation',
                defaults={
                    'category': 'CONSULTING',
                    'description': 'Initial consultation and service requirement discussion',
                    'short_description': 'Initial consultation for understanding client requirements',
                    'price': 0,
                    'duration_days': 7,
                    'is_active': True,
                    'features': ['Requirement Analysis', 'Service Planning', 'Documentation Guidance'],
                    'deliverables': ['Service Proposal', 'Timeline Estimate']
                }
            )
            
            # Determine who to assign the booking to
            assigned_to = None
            if client.assigned_sales:
                assigned_to = client.assigned_sales
            elif client.assigned_manager:
                assigned_to = client.assigned_manager
            elif self.created_by:
                assigned_to = self.created_by
            
            # Create booking with service interest in requirements
            Booking.objects.create(
                client=client,
                service=consultation_service,
                amount=Decimal('0.00'),
                final_amount=Decimal('0.00'),
                status='PENDING',
                expected_completion_date=timezone.now().date() + timedelta(days=7),
                assigned_to=assigned_to,
                created_by=self.created_by,
                priority='HIGH',
                requirements=f"Service Interest: {initial_service_text.strip()}\n\nThis is an initial consultation booking. Client has expressed interest in the above service."
            )
            
            # Also store in client notes
            client.notes = f"Initial Service Interest: {initial_service_text.strip()}"
            client.save()
        
        return client


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


class ClientProfileCompletionForm(forms.ModelForm):
    """
    Form for clients to complete their profile after initial creation.
    Allows clients to fill in business details, financial info, and address.
    """
    class Meta:
        model = Client
        fields = [
            'business_type', 'sector', 'company_age',
            'registration_number', 'gst_number', 'pan_number',
            'address_line1', 'address_line2', 'city', 'state', 'pincode',
            'annual_turnover', 'funding_required', 'existing_loans',
            'alternate_phone', 'business_description', 'funding_purpose'
        ]
        widgets = {
            'business_type': forms.Select(attrs={'class': 'form-select'}),
            'sector': forms.Select(attrs={'class': 'form-select'}),
            'company_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'placeholder': 'Years in business'
            }),
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'U12345AB2020PTC123456'
            }),
            'gst_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '22AAAAA0000A1Z5'
            }),
            'pan_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABCDE1234F'
            }),
            'address_line1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Building/Street'
            }),
            'address_line2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Locality/Area'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mumbai'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maharashtra'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '400001'
            }),
            'annual_turnover': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Annual turnover in lakhs'
            }),
            'funding_required': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Funding required in lakhs'
            }),
            'existing_loans': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Existing loans in lakhs (if any)'
            }),
            'alternate_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 9876543210'
            }),
            'business_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your business activities, products, or services'
            }),
            'funding_purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain the purpose of funding you are seeking'
            }),
        }
        help_texts = {
            'business_type': 'Select your business entity type',
            'sector': 'Select your primary business sector',
            'company_age': 'How many years has your company been operating?',
            'annual_turnover': 'Your annual business turnover (in lakhs)',
            'funding_required': 'Total funding amount you are seeking (in lakhs)',
            'existing_loans': 'Outstanding loan amount if any (in lakhs)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mark essential fields as required
        required_fields = [
            'business_type', 'sector', 'company_age',
            'address_line1', 'city', 'state', 'pincode',
            'annual_turnover', 'funding_required'
        ]
        
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
    
    def save(self, commit=True):
        """Save the profile and update status if profile is complete"""
        client = super().save(commit=False)
        
        # Check if profile is complete
        required_fields = ['business_type', 'sector', 'company_age', 'address_line1',
                          'city', 'state', 'pincode', 'annual_turnover', 'funding_required']
        
        profile_complete = all([
            getattr(client, field) for field in required_fields
        ])
        
        # Update status if profile is now complete
        if profile_complete and client.status == 'PENDING_DOCS':
            client.status = 'ACTIVE'
        
        if commit:
            client.save()
        
        return client
