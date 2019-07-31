from django.urls import path
from .views import IndexView, ExcahngeView


urlpatterns = [
    path('', IndexView.as_view()),
    path(
        "exchange_currency/",
        ExcahngeView.as_view(),
        name="exchange_currency"
        )
]
