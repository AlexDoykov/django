from django import forms


class ExchangeForm(forms.Form):
    value = forms.DecimalField()
    currency = forms.ChoiceField()
