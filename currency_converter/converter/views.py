# from decimal import Decimal
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, FormView, View

from .models import Currency
from .forms import ExchangeForm
from .customJSONEncoder import CustomJSONEncoder


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

    def get_context_data(self, **kwargs):
        kwargs['currencies'] = Currency.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # form.calculate_rate()
        response = form.cleaned_data
        return JsonResponse(response, encoder=CustomJSONEncoder)


# solution 3

def index_view(request):
    currencies = Currency.objects.all()
    form = ExchangeForm(request.POST if request.method == 'POST' else None)

    if request.method == "POST":
        # form = ExchangeForm(request.POST)
        if form.is_valid():
            # form.calculate_rate()
            response = form.cleaned_data
            return JsonResponse(response, encoder=CustomJSONEncoder)
    # if request.method == "GET":
    #     form = ExchangeForm()

    return render(
        request,
        "home.html",
        {
            'form': form,
            'currencies': currencies
        }
    )
