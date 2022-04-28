from datetime import datetime

from .models import *
from .mixins import CartMixin
from .forms import OrderForm, LoginForm, RegistrationForm
from .utils import recalc_cart
from .tasks import send_spam_email

from django.db import transaction
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView, View
from django.http import HttpResponseRedirect, JsonResponse


class BaseView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'products': products,
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'mainapp/base.html', context)


class ProductDetailView(CartMixin, DetailView):

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs.get('slug'))
        context = {
            'product': product,
            'cart': self.cart,
        }
        return render(request, 'mainapp/product_detail.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, DetailView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        category = Category.objects.get(slug=kwargs.get('slug'))
        products = Product.objects.filter(category=category)
        context = {
            'categories': categories,
            'category': category,
            'products': products,
            'cart': self.cart,
        }
        return render(request, 'mainapp/category_detail.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Товар успешно добавлен')
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Товар удален из корзины')
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'К-во изменено')
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'mainapp/cart.html', context)


class CheckoutView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.GET.get('user')
        if user and request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            data = {
                'first_name': customer.user.first_name,
                'last_name': customer.user.last_name,
                'phone': customer.phone,
                'address': customer.address,
            }
            return JsonResponse(data)
        date = request.GET.get('date')
        if date:
            data = {'is_correct': True}
            if timezone.now().date() > datetime.strptime(date, '%Y-%m-%d').date():
                data = {'is_correct': False}
            return JsonResponse(data)

        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'mainapp/checkout.html', context)


class MakeOrderView(CartMixin, View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.cust = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ')
            return HttpResponseRedirect('/')
        messages.add_message(request, messages.ERROR, 'Неправильно поле')
        return HttpResponseRedirect('/checkout')


class LoginView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'mainapp/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'mainapp/login.html', context)


class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if username:
            data = {'is_exist': User.objects.filter(username=username).exists()}
            return JsonResponse(data)

        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'mainapp/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            Customer.objects.create(user=new_user, phone=form.cleaned_data['phone'],
                                    address=form.cleaned_data['address'])

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'mainapp/registration.html', context)


class ProfileView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(cust=customer).order_by('-created_at')
        categories = Category.objects.all()
        context = {
            'orders': orders,
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'mainapp/profile.html', context)


class SupportViews(CartMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mainapp/support.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        send_spam_email.delay(email)
        return HttpResponseRedirect('/')
