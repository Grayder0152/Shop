from django.urls import path
from . import views

urlpatterns = [
    path('', views.BaseView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', views.AddToCArtView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', views.DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:ct_model>/<str:slug>/', views.ChangeQTYView.as_view(), name='change_qty'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('make-order', views.MakeOrderView.as_view(), name='make_order'),
]
