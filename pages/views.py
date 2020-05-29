from django.shortcuts import render,redirect
from .models import Item,CartItem,Order
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Contact
from .form import CheckoutForm
from .models import(
    Item,
    CartItem,
    Order,
    ShippingAddress,
    BillingAddress,
    Payment
)

def index(request):
    items = Item.objects.all().order_by('-id')
    paginator = Paginator(items, 12)
    
    page = request.GET.get('page')
    
    items_page_object = paginator.get_page(page)
    context = {
        'items':items_page_object,
        'title':'Home'
    }
    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html', {'title':'About'})

def product(request, id):
    item = get_object_or_404(Item, id=id)
    cat_items = Item.objects.filter(category = item.category).exclude(id=item.id)
    context = {
        'item':item,
        'cat_items':cat_items,
        'title':item.title
    }
    return render(request, 'pages/product.html',context)
@login_required
def cart(request):
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
    context = {
        'subtotal':Subtotal,
        'shipping':Shipping,
        'total':total,
        'cart_items':all_cart_items,
        'title':'Cart'
    }
    return render(request, 'pages/cart.html', context)

@login_required
def add_to_cart(request,id):
    item  = get_object_or_404(Item, id=id)
    cart_item, created = CartItem.objects.get_or_create (
        user = request.user,
        item = item
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the Cartitem is in the Order
        if order.cart_items.filter(item__id=item.id).exists():
            cart_item.quantity += 1
            cart_item.save()
            return redirect('cart')
        else:
            order.cart_items.add(cart_item)
            messages.success(request, 'Item has been successfully added to your cart')
            return redirect('product', item.id)

    else:
        order = Order.objects.create(user=request.user, ordered=False)
        order.cart_items.add(cart_item)
        messages.success(request, 'Item has been successfully added to your cart')
        return redirect('product', item.id)
    
        
def remove_from_cart(request, id):
    item = get_object_or_404(CartItem, id=id)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        return redirect('cart')
    else:
        CartItem.delete(item)
        order.cart_items.remove(item)
        return redirect('cart')
def checkout(request):
    if request.method =='POST':
        form = CheckoutForm(request.POST)
        cart_items = CartItem.objects.filter(user=request.user)
        order = Order.objects.get(user=request.user, ordered=False)
        if form.is_valid():
            shipping_address = form.cleaned_data.get('shipping_address')
            shipping_address2 = form.cleaned_data.get('shipping_address2') 
            country = form.cleaned_data.get('country') 
            city = form.cleaned_data.get('city') 
            payment_option = form.cleaned_data.get("payment_option")
            use_default_address = form.cleaned_data.get('use_default_address')
            
            shipping_add_qs = ShippingAddress.objects.filter(user=request.user)
            if use_default_address:
                shipping_qs = ShippingAddress.objects.filter(user=request.user)
                if shipping_qs.exists():
                    shipping_address = shipping_qs[0]
                    order.shipping_address= shipping_address
                    order.save() 
                else:
                    return redirect('checkout')
            # check if the user has an existing address if yes update the previous
            elif shipping_add_qs.exists():
                prev_address = shipping_add_qs[0]
                prev_address = shipping_add_qs.update(
                    user=request.user,
                    street_address = shipping_address,
                    apartment_address = shipping_address2,
                    country= country,
                    city = city
                )
                order.save(update_fields=['shipping_address'])
            # if no address exists create a new one
            else:
                new_shipping_addr = ShippingAddress.objects.create(
                    user=request.user,
                    street_address = shipping_address,
                    apartment_address = shipping_address2,
                    country= country,
                    city = city
                )
                order.shipping_address = new_shipping_addr
                order.save()
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
            context = {
                'cartitems':all_cart_items,
                'subtotal':Subtotal,
                'total_qty':cart_quantity,
                'shipping':Shipping,
                'total':total,
                'cart_items':all_cart_items,
                'title':'Payment'
            }
           
            if payment_option == 'S':
                 return render(request, 'payment/stripe.html', context)
            elif payment_option == 'P':
                return render(request, 'pages/paypal.html', context)
            else:
                return render(request, 'pages/cash.html')
            
    else:
        form = CheckoutForm()
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
        context = {
            'cartitems':all_cart_items,
            'subtotal':Subtotal,
            'total_qty':cart_quantity,
            'shipping':Shipping,
            'total':total,
            'cart_items':all_cart_items,
            "form":form,
            'title':'Checkout'
        }
        return render(request, 'pages/checkout.html', context)
def stripe(request):
    return render(request, 'pages/payment.html')
def paypal(request):
    return render(request, 'pages/paypal.html')
def cash(request):
    return render(request, 'pages/cash.html')

def fashion(request):
    fashion = Item.objects.filter(category = 'FS')
    context = {
        'fashion':fashion,
        'title':'Fashion'
    }
    return render(request, 'pages/fashion.html', context)
def furniture(request):
    furniture = Item.objects.filter(category = 'FT')
    context = {
        'furniture':furniture,
        'title':'Furniture'
    }
    return render(request, 'pages/furniture.html', context)
# @login_required
# def buynow(request,id):
#         item = get_object_or_404(Item, id=id)
#         # order_item, created = Order.objects.get_or_create (
#         #     user=request.user,
#         #     item=item 
#         # )
#         # if Order.objects.filter(user=request.user, item__id=item.id).exists():
#         #     return redirect('checkout')
#         # else:
#         #     order_item.save()
#         # print(order_item)
#         subtotal = item.item_price()
#         shipping = item.get_shipping_cost()
#         total = item.get_final_price()
#         print(total)
#         context ={
#             'item':item,
#             'subtotal':subtotal,
#             'shipping':shipping,
#             'total':total
#         }
#         return render(request, 'pages/buynow.html', context)
def search(request):
    keyword = request.GET['keyword']
    search_items = Item.objects.filter(title__icontains = keyword)
    context = {
        'items':search_items,
        'value': request.GET,
        'title':keyword
    }
    return render(request, 'pages/search.html', context)
def contact(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        Contact.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone, message=message)
        return redirect('index')
    return render(request, 'pages/contact.html', {'title':'Contact'})