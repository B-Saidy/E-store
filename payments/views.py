from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
import stripe
from pages.models import CartItem
stripe.api_key = settings.STRIPE_SECRET_KEY

def total(request):
    all_cart_items = CartItem.objects.filter(user = request.user)
    Subtotal = 0
    Shipping = 0
    cart_quantity=0
    total = 0
    for item in all_cart_items:
        Subtotal += item.get_cart_item_price()
        cart_quantity += item.quantity
        Shipping += item.get_shipping()
        total += item.get_total_price()
    return total

def charge(request):
    if request.method == 'POST':
            
        token = request.POST['stripeToken']
        print('Data', request.POST)

        stripe.Customer.create(
        description="My First Test Customer",
        email = request.POST['email']
        )
        
        stripe.Charge.create(
        amount=int(total(request)*100),
        currency="usd",
        source=token,
        description="My Test Charge",
        )
        return render(request, 'payment/charge.html', {'total':total(request)})
    return render(request, 'payment/stripe.html')