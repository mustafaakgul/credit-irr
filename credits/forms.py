from django.forms import ModelForm, NumberInput, TextInput
from django import forms

from credits.models import IRRTable, Financial


class IRRTableForm(ModelForm):
    class Meta:
        model = IRRTable

        exclude = ()

        widgets = {
            'index': NumberInput(attrs={'class': 'formset-field form-control'}),
            'amount': NumberInput(attrs={'class': 'formset-field form-control'}),
        }

class FinancialForm(forms.Form):
    class Meta:
        model = Financial

        exclude = ()

        widgets = {
            'total_amount': TextInput(attrs={'class': 'formset-field form-control'}),
        }