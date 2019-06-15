from django import forms
from .models import Currency
from decimal import Decimal
from django.core.validators import MinValueValidator


class ExchangeForm(forms.Form):
    value = forms.DecimalField(
            validators=[MinValueValidator(Decimal('0.00'))]
            )
    currency = forms.ChoiceField()
    converted_value = forms.DecimalField(
            disabled=True,
            required=False
            )
    value.widget.attrs.update({'id': 'value'})
    currency.widget.attrs.update({'id': 'currency'})
    converted_value.widget.attrs.update({'id': 'converted_value'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["currency"].choices = [
                (c.id, c.name)
                for c in Currency.objects.all().order_by("name")
                ]
