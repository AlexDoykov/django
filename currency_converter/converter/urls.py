from django.urls import path
from .views import IndexView, ExchangeView, ExchangeFormView, index_view


urlpatterns = [
    path('', ExchangeFormView.as_view()),
    path(
        "exchange_currency/",
        ExchangeFormView.as_view(),
        name="exchange_currency"
        )
]
