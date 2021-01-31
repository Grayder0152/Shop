from django.urls import path
from .views import BaseSpacView


urlpatterns = [
    path('', BaseSpacView.as_view(), name='base-spec'),
]