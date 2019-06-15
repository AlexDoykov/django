from django import forms
from .models import Currency


class ExchangeForm(forms.Form):
    value = forms.DecimalField()
    currency = forms.ChoiceField(choices=[(c.id, c.name) for c in Currency.objects.all().order_by("name")])

   # def __init__(self, *args, **kwargs):
   #     super(ExchangeForm, self).__init__(*args, **kwargs)
   #     choices = [(c.id, c.name) for c in Currency.objects.all().order_by("name")]
   #     self.fields['currency'].choices = choices 
