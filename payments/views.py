from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
import stripe
from pages.models import CartItem
stripe.api_key = settings.STRIPE_SECRET_KEY

class HomePageView(TemplateView):
    
    template_name = 'payment/stripe.html'
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context 
    
# def charge(request): # new
#     if request.method == 'POST':
#         all_cart_items = CartItem.objects.filter(user = request.user)
#         Subtotal = 0
#         Shipping = 0
#         cart_quantity=0
#         total = 0
#         for item in all_cart_items:
#             Subtotal += item.get_cart_item_price()
#             cart_quantity += item.quantity
#             Shipping += item.get_shipping()
#             total += item.get_total_price()
#         charge = stripe.Charge.create(
#             amount=total*100,  # amount charge in cent
#             currency='usd',
#             description='A Django charge',
#             source=request.POST['stripeToken']
#         )
#         return render(request, 'payment/charge.html')

def charge(request): # new
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,  # amount charge in cent
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'payment/charge.html')