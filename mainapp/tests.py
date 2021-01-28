from django.test import TestCase, Client, RequestFactory
from .models import *
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from .views import recalc_cart, AddToCartView

User = get_user_model()


class ShopTestCases(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='12345')
        self.category = Category.objects.create(name='Ноутбуки', slug='notebook')
        image = SimpleUploadedFile('iphone.jpg', content=b'', content_type='media/')
        self.notebook = Notebook.objects.create(
            category=self.category,
            title='Test',
            image=image,
            price=Decimal('50000.00'),
            diagonal='17.3',
            display_type='IPS',
            processor_freq='3.4',
            ram='6 Gb',
            video='GTX',
            time_without_charge='10'
        )
        self.customer = Customer.objects.create(user=self.user, phone='112121', address='Adres')
        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            content_object=self.notebook
        )

    def test_add_to_cart(self):
        self.cart.products.add(self.cart_product)
        recalc_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.products.all())
        self.assertEqual(self.cart.products.count(), 1)
        self.assertEqual(self.cart.final_price, Decimal('50000.00'))

    def test_response(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        response = AddToCArtView.as_view()(request, ct_model='notebook', slug='test-slug')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')
