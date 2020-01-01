from django.contrib import admin
from . models import Item,CartItem, Order, Contact, BillingAddress, ShippingAddress, Payment,Refund
# Register your models here.
admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Contact)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Refund)