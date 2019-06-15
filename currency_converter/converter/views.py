from django.shortcuts import render
from .models import Currency
from .forms import ExchangeForm
from django.http import HttpResponseRedirect


def process_exchange_form():
    pass


def index(request):
    currencies = Currency.objects.all().order_by("name")

    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        if form.is_valid():
            process_exchange_form()
            return HttpResponseRedirect("")
    else:
        form = ExchangeForm()

    template_data = {
        "exchange_form": form,
        "all_currencies": currencies,
    }

    return render(request, 'home.html', template_data)
