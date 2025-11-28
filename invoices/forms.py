from django import forms
from datetime import date
from .models import Invoice
from clients.models import Client

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'invoice_type',
            'client',
            'issue_date',
            'due_date',
            'item_description',
            'hsn_sac',
            'gst_rate',
            'quantity',
            'rate',
            'place_of_supply',
            'place_of_supply_code',
            'notes',
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # sirf apne assigned clients dikhao (Client model me: assigned_sales)
        if user is not None:
            self.fields['client'].queryset = Client.objects.filter(assigned_sales=user)

        if not self.initial.get('issue_date'):
            self.initial['issue_date'] = date.today()
