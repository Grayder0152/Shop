from django.urls import path
from .views import BaseSpacView,NewCategoryView


urlpatterns = [
    path('', BaseSpacView.as_view(), name='base-spec'),
    path('new-category', NewCategoryView.as_view(), name='new_category'),
]