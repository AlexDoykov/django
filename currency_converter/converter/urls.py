from django.urls import path
from .views import IndexView, ExcahngeView, ExchangeFormView


urlpatterns = [
    path('', IndexView.as_view()),
    path(
        "exchange_currency/",
        ExchangeFormView.as_view(),
        name="exchange_currency"
        )
]
