from django import forms
from .models import Currency
from decimal import Decimal
from django.core.validators import MinValueValidator


class ExchangeForm(forms.Form):
    value = forms.DecimalField(validators=[MinValueValidator(Decimal('0.00'))])
    currency = forms.ChoiceField(choices=[(c.id, c.name) for c in Currency.objects.all().order_by("name")])
    converted_value = forms.DecimalField(disabled=True, required=False)
