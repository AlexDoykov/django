from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _

from .models import Currency


class ExchangeForm(forms.Form):
    currency_from = forms.ModelChoiceField(
        label=_('currency from'),
        queryset=Currency.objects.all(),
        )
    currency_to = forms.ModelChoiceField(
            label=_('currency to'),
            queryset=Currency.objects.all()
            )
    amount = forms.DecimalField(
            label=_('amount'),
            validators=[MinValueValidator(Decimal('0.00'))]
            )
    converted_amount = forms.DecimalField(
            label=_('converted amount'),
            disabled=True,
            required=False
            )
    amount.widget.attrs.update({'id': 'amount'})
    currency_from.widget.attrs.update({'id': 'currency_from'})
    currency_to.widget.attrs.update({'id': 'currency_to'})
    converted_amount.widget.attrs.update({'id': 'converted_amount'})

    def clean_converted_amount(self):
        try:
            from_rate = self.cleaned_data['currency_from'].get_latest_rate()
            to_rate = self.cleaned_data['currency_to'].get_latest_rate()
            amount = self.cleaned_data['amount']
        except KeyError:
            pass
        else:
            base_amount = from_rate * amount
            return base_amount / to_rate
