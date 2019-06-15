from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'exchange_currency/',
        views.exchange_currency,
        name="exchange_currency"
        )
]
