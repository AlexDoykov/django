from django.shortcuts import render
from .models import Currency
from .forms import ExchangeForm
from django.http import HttpResponseRedirect
from decimal import Decimal


def process_exchange_form(cleared_form):
    currency_object = Currency.objects.get(id=cleared_form['currency'])
    exchange_rate = currency_object.exchange_rate
    value = cleared_form['value']
    form_values = {
            'converted_value': exchange_rate * Decimal(value),
            'value': value,
            'currency': cleared_form['currency']
            }
    return ExchangeForm(initial=form_values)


def index(request):
    currencies = Currency.objects.all().order_by("name")

    template_data = {
        "all_currencies": currencies,
    }

    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        if form.is_valid():
            form = process_exchange_form(form.cleaned_data)
    else:
        form = ExchangeForm()
    template_data["exchange_form"] = form

    return render(request, 'home.html', template_data)
