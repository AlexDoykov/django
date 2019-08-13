from django.urls import path

from .views import ExchangeFormView, CurrencyDetailView

app_name = 'converter'
urlpatterns = [
    path('', ExchangeFormView.as_view()),
    path(
        'exchange_currency/',
        ExchangeFormView.as_view(),
        name='exchange_currency'
        ),
    path(
        '<int:pk>/',
        CurrencyDetailView.as_view(),
        name='currency_detail_view'
        )
]
