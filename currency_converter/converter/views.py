from django.shortcuts import render
from .models import Currency
from .forms import ExchangeForm
from django.http import HttpResponse
from decimal import Decimal
import json


def exchange_currency(request):
    if request.method == 'POST':
        value = request.POST.get('value')
        currency_from = request.POST.get('currency_from')
        currency_to = request.POST.get('currency_to')
        currency_object = Currency.objects.get(id=currency_from)
        exchange_rate = currency_object.exchange_rate
        form_values = {
            'converted_value': float(exchange_rate * Decimal(value)),
            'value': value,
            'currency_from': currency_from,
            'currency_to': currency_to,
            }

        return HttpResponse(
            json.dumps(form_values),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def index(request):
    currencies = Currency.objects.all().order_by("name")

    template_data = {
        "all_currencies": currencies,
    }

    template_data["exchange_form"] = ExchangeForm()

    return render(request, 'home.html', template_data)
