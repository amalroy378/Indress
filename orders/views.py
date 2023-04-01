from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import CartItem,Cart
from .forms import OrderForm
from .models import Order,OrderProduct,Payment
import datetime
import razorpay
from django.conf import settings

# Create your views here.
def place_order(request,total=0,quantity=0):
    current_user=request.user

    #if the cart count is lessthan or equal to zero ,then redirect to home
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count<=0:
        return redirect('home')
    
    total=0
    for cart_item in cart_items:
        total+=(cart_item.product.price * cart_item.quantity)
        quantity+=cart_item.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #store all the order iinformation inside the order table
            data = Order()
            
            data.user = current_user

            data.first_name=form.cleaned_data['first_name']

            data.last_name=form.cleaned_data['last_name']

            data.phone_name=form.cleaned_data['phone']

            data.email_name=form.cleaned_data['email']
            
            data.address_line_1=form.cleaned_data['address_line_1']
            
            data.address_line_2=form.cleaned_data['address_line_2']

            data.country=form.cleaned_data['country']

            data.state=form.cleaned_data['state']

            data.city=form.cleaned_data['city']

            data.order_note=form.cleaned_data['order_note']

            data.order_total= total

        
            data.ip = request.META.get('REMOTE_ADDR')

            data.save()

            #generate order number

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()


            return redirect('checkout')
        else:
            return redirect('checkout')




def order_show(request):

        # orderproduct =OrderProduct.objects.filter(user=request.user)
        context={


        # 'orderproduct': orderproduct,
        }

        return render(request,'order_show.html',context)