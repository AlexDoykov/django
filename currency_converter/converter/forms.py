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

    # def clean(self):
    #     self.cleaned_data["converted_value"] = self.clean_converted_value()

    def clean_converted_value(self):
        try:
            from_rate = self.cleaned_data["currency_from"].exchange_rate
            to_rate = self.cleaned_data["currency_to"].exchange_rate
            value = self.cleaned_data["value"]
        except KeyError:
            pass
        else:
            base_value = from_rate * value
            return base_value / to_rate
