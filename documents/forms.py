from django import forms
from .models import Document
from clients.models import Client

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'title', 'description', 'document_number']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Optional description'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter document number/reference'}),
        }

    def clean_document_number(self):
        doc_num = self.cleaned_data.get('document_number')
        if not doc_num:
            raise forms.ValidationError('Please enter a document number.')
        return doc_num


class SalesDocumentUploadForm(forms.ModelForm):
    """Form for sales employees to upload documents for their clients"""
    
    class Meta:
        model = Document
        fields = ['client', 'document_type', 'title', 'description', 'document_number']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Optional description'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter document number/reference'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Limit client choices to those assigned to or created by this sales user
            from django.db.models import Q
            self.fields['client'].queryset = Client.objects.filter(
                Q(assigned_sales=user) | Q(created_by=user)
            ).order_by('company_name')
    
    def clean_document_number(self):
        doc_num = self.cleaned_data.get('document_number')
        if not doc_num:
            raise forms.ValidationError('Please enter a document number.')
        return doc_num
