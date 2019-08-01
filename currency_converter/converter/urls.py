from django.urls import path
from .views import IndexView, ExcahngeView, ExchangeFormView, index_view


urlpatterns = [
    path('', index_view),
    path(
        "exchange_currency/",
        index_view,
        name="exchange_currency"
        )
]
