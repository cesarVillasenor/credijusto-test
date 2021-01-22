from django.urls import path
from .api.viewsets import UserCountView

urlpatterns = [
    path('api/', UserCountView.as_view()),
]

