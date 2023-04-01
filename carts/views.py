from django.shortcuts import render,redirect,get_object_or_404
from eachcategorypages.models import Product
from app.models import Variation
from .models import CartItem,Cart  
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist 

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from userprofile.models import Account,Address
import razorpay
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from  orders.models import Order


# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart    


# def add_cart(request,product_id):
#     current_user = request.user
#     product = Product.objects.get(id=product_id) # get the product
#     product_variation = []
#     if request.method=='POST':
#          for item in request.POST:
#                 key = item
#                 value = request.POST[key]


#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except:
#                     pass

#     if current_user.is_authenticated:
        
#         cart,_ = Cart.objects.get_or_create(cart_id=_cart_id(request),user = current_user)
#         # usr = Account.objects.get(username = request.user)
#         is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
#         if is_cart_item_exists:
#             cart_item = CartItem.objects.get(product=product,user=current_user)
#             cart_item.quantity+=1 #incrementing the quantity of prodiuct presnet in the cart
#         else:
#             cart_item = CartItem.objects.create( #if not exist it will create one cart
#             cart = cart,
#             product=product,
#             user = current_user,
#             quantity = 1
#         )
#         cart_item.save()
    
#     else:

    
#         try:
#             cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using cart_id present in the session
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(
#                 cart_id = _cart_id(request)
#             )
#             cart.save()
        
#         try:
#             cart_item = CartItem.objects.get(product=product, cart=cart)
#             if len(product_variation)>0:
#                 cart_item.variations.clear()
#                 for item in product_variation:
#                     cart_item.variations.add(item)
#             cart_item.quantity += 1
#             cart_item.save()
#         except CartItem.DoesNotExist:
#             cart_item = CartItem.objects.create(
#                 product = product,
#                 quantity = 1,
#                 cart = cart,
#             )
#             if len(product_variation)>0:
#                 cart_item.variations.clear()
#                 for item in product_variation:
#                     cart_item.variations.add(item) 
#             cart_item.save()
#     return redirect('cart')


def add_cart(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) # get the product
    product_variation = []
    if request.method=='POST':
         for item in request.POST:
                key = item
                value = request.POST[key]


                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

    if current_user.is_authenticated:
        
        cart,_ = Cart.objects.get_or_create(cart_id=_cart_id(request),user = current_user)
        # usr = Account.objects.get(username = request.user)
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(product=product,user=current_user)
            if cart_item.quantity >= product.stock:
                messages.warning(request, "Sorry, the product is out of stock.")
                return redirect('cart')
            cart_item.quantity+=1 #incrementing the quantity of prodiuct presnet in the cart
        else:
            cart_item = CartItem.objects.create( #if not exist it will create one cart
            cart = cart,
            product=product,
            user = current_user,
            quantity = 1
        )
        cart_item.save()
    
    else:

    
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()
        
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            if len(product_variation)>0:
                cart_item.variations.clear()
                for item in product_variation:
                    cart_item.variations.add(item)
            if cart_item.quantity >= product.stock:
                messages.warning(request, "Sorry, the product is out of stock.")
                return redirect('product_detail', product_id=product.id)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation)>0:
                cart_item.variations.clear()
                for item in product_variation:
                    cart_item.variations.add(item) 
            cart_item.save()
    return redirect('cart')








def cart(request,total=0,quantity=0,cart_items=None):
    
    
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)

        else:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            quantity+=cart_item.quantity

    except ObjectDoesNotExist:
        pass  

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,

    }      
    return render(request,'cart.html',context)










def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity-=1
        cart_item.save()

    else:
        cart_item.delete()
    return redirect('cart')  



def remove_cart_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.filter(product=product,cart=cart)
    
    cart_item.delete()
    return redirect('cart')




@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):

    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        

        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            quantity+=cart_item.quantity

    except ObjectDoesNotExist:
        pass  

    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    payment = client.order.create({'amount': total*100, 'currency': 'INR', 'payment_capture': 1})

    context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'name': request.user,
            'payment':payment,
            
        }

    return render(request,'checkout.html',context)
    

def success_page(request):
        return render(request,'success_page.html')


def cod(request,total=0,quantity=0,cart_items=None):

    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)

        order =Order.objects.filter(user=request.user).last()

        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            quantity+=cart_item.quantity

    except ObjectDoesNotExist:
        pass  

    context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'name': request.user,
            'order':order,
        }

    if request.method == 'POST':
        # Perform the cash on delivery logic here
        # Set up your success and error URLs
       

       return render(request,'cod.html',context) 
