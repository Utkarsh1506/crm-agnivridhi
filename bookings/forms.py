from django import forms
from django.contrib.auth import get_user_model
from .models import Booking, ServiceDocumentRequirement
from documents.models import Document

User = get_user_model()


class DocumentCollectionForm(forms.Form):
    """
    Dynamic form for collecting documents required by a service
    """
    
    def __init__(self, booking, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.booking = booking
        
        # Get required documents for this service
        required_docs = booking.get_required_documents()
        
        for doc_req in required_docs:
            field_name_number = f"doc_{doc_req.id}_number"
            field_name_file = f"doc_{doc_req.id}_file"
            field_name_notes = f"doc_{doc_req.id}_notes"
            
            # Document number/reference field
            self.fields[field_name_number] = forms.CharField(
                label=f"{doc_req.get_document_type_display()} - Reference Number",
                required=doc_req.is_mandatory,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g., GST/HR/12345',
                    'data-doc-id': str(doc_req.id),
                }),
                help_text=doc_req.description if doc_req.description else ''
            )
            
            # File upload field
            self.fields[field_name_file] = forms.FileField(
                label=f"Upload {doc_req.get_document_type_display()}",
                required=doc_req.is_mandatory,
                widget=forms.FileInput(attrs={
                    'class': 'form-control',
                    'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx',
                    'data-doc-id': str(doc_req.id),
                }),
                help_text='Accepted formats: PDF, JPEG, PNG, DOC, DOCX'
            )
            
            # Optional notes
            self.fields[field_name_notes] = forms.CharField(
                label=f"Notes for {doc_req.get_document_type_display()} (Optional)",
                required=False,
                widget=forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 2,
                    'placeholder': 'Any additional notes about this document...',
                    'data-doc-id': str(doc_req.id),
                }),
            )


class QuickDocumentUploadForm(forms.Form):
    """
    Simpler form for quick document uploads with document number and file
    """
    document_type = forms.ChoiceField(
        label='Document Type',
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=Document.DocumentType.choices
    )
    
    reference_number = forms.CharField(
        label='Document Reference Number',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., GST/HR/12345',
        })
    )
    
    file = forms.FileField(
        label='Upload Document',
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx',
        })
    )
    
    notes = forms.CharField(
        label='Notes (Optional)',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Any additional notes...',
        })
    )
