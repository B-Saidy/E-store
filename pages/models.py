from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.utils import timezone

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

CATEGORY_CHOICE = (
    ('FS','Fashion'),
    ('ET','Electronics'),
    ('FT','Furniture'),
    ('PT','Phones & Tablets'),
)
LABEL_CHOICE = (
    ('P','primary'),
    ('S','secondary'),
    ('D','danger')  
)

TREND_CHOICE = (
    ('N',"NEW"),
    ('H','HOT'),
    ('S','SALE')
)
class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'Shipping Addresses'
        
class Item(models.Model):
    title = models.CharField(max_length = 100)
    description  = models.CharField(max_length = 200)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    category = models.CharField(choices = CATEGORY_CHOICE, max_length= 2)
    label = models.CharField(choices = LABEL_CHOICE, max_length= 2, blank = True, null=True)
    trend = models.CharField(choices = TREND_CHOICE, max_length= 2, blank = True, null=True)
    image = models.ImageField(upload_to = 'photos', blank = True, null=True)
    photo_1 = models.ImageField(default='2.jpg', upload_to = 'photos')
    photo_2 = models.ImageField(default='2.jpg', upload_to = 'photos')
    photo_3 = models.ImageField(default='2.jpg', upload_to = 'photos')
    photo_4 = models.ImageField(default='2.jpg', upload_to = 'photos')
    photo_5 = models.ImageField(default='2.jpg', upload_to = 'photos')
    weight = models.FloatField(blank=True, null=True, default=1)
    volume = models.FloatField(blank=True, null=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("product", kwargs={"id": self.id})
    
    def add_item_to_cart(self):
        return reverse("add_to_cart", kwargs={"id": self.id})
    
    def item_price(self): 
        if self.discount_price:
            return self.discount_price
        return self.price
    def get_shipping_cost(self):
        if self.weight:
            return self.weight*10
        return self.volume*100
    def get_final_price(self):
        return self.get_shipping_cost() + self.item_price()
    def get_discount_percent(self):
        return round((self.price-self.discount_price)/self.price*100)
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.item.title
    def remove_from_cart(self):
        return reverse("remove_from_cart", kwargs={"id": self.id})
    def get_shipping(self):
        return self.item.get_shipping_cost() * self.quantity
    def get_unit_item_price(self):
        return self.item.item_price()
    def get_cart_item_price(self):
        return self.item.item_price()*self.quantity
    # def get_total_unit_price(self):
    #     return self.item.price*self.quantity
    def get_total_price(self):
        return self.get_cart_item_price() + self.get_shipping()
           
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem,blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.OneToOneField(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    # billing_address = models.ForeignKey(
    #     'BillingAddress', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def get_cart_item_total(self):
        total=0
        for item in self.cart.all():
            total += self.cart.get_total_price()
            return total
        
    def get_unit_item_price(self):
        return self.item.get_final_price() 
    
    
class Contact(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email= models.CharField(max_length = 50)
    phone = models.IntegerField()
    message = models.TextField(max_length = 500)
    def __str__(self):
        return self.first_name

class BillingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'Billing Addresses'

        
class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    def __str__(self):
        return f"{self.pk}"