from django.urls import path
from .views import IndexView, exchange_currency


urlpatterns = [
    path('', IndexView.as_view()),
    path(
        "exchange_currency/",
        exchange_currency,
        name="exchange_currency"
        )
]
