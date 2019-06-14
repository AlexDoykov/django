from django.shortcuts import render
from .models import Currency, ExchangeRate


def index(request):
    data = ExchangeRate.objects.all()

    currency_rate = {
        "currency_rate": data
    }

    return render(request, 'home.html', currency_rate)
