from django import forms
from .models import Document
from clients.models import Client

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'title', 'description', 'file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Optional description'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if not f:
            raise forms.ValidationError('Please select a file to upload.')
        # Optional: limit file size to 25MB
        max_mb = 25
        if f.size > max_mb * 1024 * 1024:
            raise forms.ValidationError(f'File too large. Max size is {max_mb} MB.')
        return f


class SalesDocumentUploadForm(forms.ModelForm):
    """Form for sales employees to upload documents for their clients"""
    
    class Meta:
        model = Document
        fields = ['client', 'document_type', 'title', 'description', 'file']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Optional description'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Limit client choices to those assigned to or created by this sales user
            from django.db.models import Q
            self.fields['client'].queryset = Client.objects.filter(
                Q(assigned_sales=user) | Q(created_by=user)
            ).order_by('company_name')
    
    def clean_file(self):
        f = self.cleaned_data.get('file')
        if not f:
            raise forms.ValidationError('Please select a file to upload.')
        max_mb = 25
        if f.size > max_mb * 1024 * 1024:
            raise forms.ValidationError(f'File too large. Max size is {max_mb} MB.')
        return f
