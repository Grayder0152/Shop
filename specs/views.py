from django.views import View
from django.shortcuts import render

class BaseSpacView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'specs/product_features.html', {})




