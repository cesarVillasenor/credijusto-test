from django.urls import path
from .api.viewsets import RatesView

urlpatterns = [
    path('api/', RatesView.as_view()),
]

