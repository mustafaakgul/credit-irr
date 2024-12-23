from django.forms import ModelForm, NumberInput, TextInput

from credit.models import IRRTable


class IRRTableForm(ModelForm):
    class Meta:
        model = IRRTable
        exclude = ('amount', )
        # widgets = {
        #     'index': NumberInput(attrs={'class': 'form-control'}),
        #     'index_type': TextInput(attrs={'class': 'form-control'}),
        #     'amount': NumberInput(attrs={'class': 'form-control'}),
        # }