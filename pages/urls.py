from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('about/',views.about, name='about'),
    path('cart/',views.cart, name='cart'),
    path('add/<int:id>',views.add_to_cart, name='add_to_cart'),
    path('remove/<int:id>',views.remove_from_cart, name='remove_from_cart'),
    path('<int:id>/',views.product, name='product'),
    path('checkout/',views.checkout, name='checkout'),
    path('fashion/',views.fashion, name='fashion'),
    path('furniture/',views.furniture, name='furniture'),
    # path('<int:id>/buynow/',views.buynow, name='buynow'),
    path('search/',views.search, name='search'),
    path('checkout/stripe/',views.stripe, name='stripe'),
    path('checkout/paypal/',views.paypal, name='paypal'),
    path('checkout/cash/',views.cash, name='cash'),
    path('contact/',views.contact, name='contact'),
]

