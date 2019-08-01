from django import forms
from .models import Currency
from decimal import Decimal
from django.core.validators import MinValueValidator


class ExchangeForm(forms.Form):
    currency_from = forms.ModelChoiceField(
        label="Валута от",
        queryset=Currency.objects.all()
        )
    currency_to = forms.ModelChoiceField(
            label="Валута в",
            queryset=Currency.objects.all()
            )
    value = forms.DecimalField(
            validators=[MinValueValidator(Decimal('0.00'))],
            label='Сума')
    converted_value = forms.DecimalField(
            disabled=True,
            required=False
            )
    value.widget.attrs.update({'id': 'value'})
    currency_from.widget.attrs.update({'id': 'currency_from'})
    currency_to.widget.attrs.update({'id': 'currency_to'})
    converted_value.widget.attrs.update({'id': 'converted_value'})

    def calculate_rate(self):
        currency_from_rate = self.cleaned_data["currency_from"].exchange_rate
        currency_to_rate = self.cleaned_data["currency_to"].exchange_rate
        value = self.cleaned_data["value"]
        self.cleaned_data["value"] = 37
        currency_from_converted_to_levs = currency_from_rate * value
        currency_to_converted = currency_from_converted_to_levs / currency_to_rate
        self.cleaned_data["converted_value"] = currency_to_converted
        print(self.cleaned_data["converted_value"])
