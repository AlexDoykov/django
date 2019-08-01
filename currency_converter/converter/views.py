from django.shortcuts import render
from django.views.generic import ListView, FormView, View
from .models import Currency
from .forms import ExchangeForm
from django.http import HttpResponse
from .customJSONEncoder import CustomJSONEncoder
# from decimal import Decimal
import json


# solution one

class IndexView(ListView, FormView):
    template_name = "home.html"
    model = Currency
    context_object_name = "currencies"

    form_class = ExchangeForm


class ExchangeView(View):
    template_name = "home.html"
    success_url = "/"

    def post(self, request):
        print(request.POST.get("currency_from"))
        form = ExchangeForm(request.POST)
        response = {}
        if form.is_valid():
            form.calculate_rate()
            response = form.cleaned_data
            return HttpResponse(
                json.dumps(response, cls=CustomJSONEncoder),
                content_type="application/json"
                )
        return HttpResponse(
                json.dumps(response, cls=CustomJSONEncoder),
                content_type="application/json"
                )


# solution 2

class ExchangeFormView(FormView):
    form_class = ExchangeForm
    template_name = "home.html"
    success_url = "/"

    def currencies(self):
        return Currency.objects.all()

    def form_valid(self, form):
        form.calculate_rate()
        response = form.cleaned_data
        return HttpResponse(
                json.dumps(response, cls=CustomJSONEncoder),
                content_type="application/json"
                )


# solution 3

def index_view(request):
    currencies = Currency.objects.all()

    if request.method == "POST":
        form = ExchangeForm(request.POST)
        if form.is_valid():
            form.calculate_rate()
            response = form.cleaned_data
            return HttpResponse(
                json.dumps(response, cls=CustomJSONEncoder),
                content_type="application/json"
                )
    if request.method == "GET":
        form = ExchangeForm()

    return render(
        request,
        "home.html",
        {
            'form': form,
            'currencies': currencies
        }
    )
