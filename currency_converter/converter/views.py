from django.shortcuts import render
from django.views.generic import ListView, FormView, View
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


class ExcahngeView(View):
    def post(self, request):
        form = ExchangeForm(request.POST)
        if form.is_valid():
            converted = form.calculate_rate()
            response = request.POST.dict()
            response["converted_value"] = str(converted)
            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
            )
        else:
            print("OOOOPPPSSSSS")


class ExchangeFormView(FormView):
    form_class = ExchangeForm
    template_name = "home.html"
    success_url = "/"
    def form_valid(self, form):
        form.calculate_rate()
        return super().form_valid(form)
