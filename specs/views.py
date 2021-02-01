from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NewCategoryForm

class BaseSpacView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'specs/product_features.html', {})


class NewCategoryView(View):

    def get(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {
            'form':form
        }
        return render(request, 'specs/new_category.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {'form':form}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/product-specs/')
        return render(request, 'specs/new_category.html', context)





























