from django.shortcuts import render
from django.views.generic import ListView, FormView
from .models import Currency
from .forms import ExchangeForm
from django.http import HttpResponse
# from decimal import Decimal
import json


class IndexView(ListView, FormView):
    template_name = "home.html"
    model = Currency
    context_object_name = "currencies"

    form_class = ExchangeForm

    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)


def exchange_currency(request):
    if request.method == "POST":
        form = ExchangeForm(request.POST)
        if form.is_valid():
            form.calculate_rate()

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

    template_data = {}

    template_data["exchange_form"] = ExchangeForm()

    return render(request, 'home.html', template_data)
