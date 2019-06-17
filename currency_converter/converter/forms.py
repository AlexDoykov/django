from django import forms
from .models import Currency
from decimal import Decimal
from django.core.validators import MinValueValidator


class ExchangeForm(forms.Form):
    currency_from = forms.ChoiceField(label='Валута от')
    currency_to = forms.CharField(
            max_length=4,
            label='Валута в',
            initial="Лева",
            disabled=True
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["currency_from"].choices = [
                (c.id, c.name)
                for c in Currency.objects.all().order_by("name")
                ]
