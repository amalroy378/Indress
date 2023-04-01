from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import auth,User
from django.contrib import messages
from .models import Profile,  carousel_Home,Banner
from django.http import HttpResponse


import requests
from .models import dress
from .models import UserOTP
import random
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
from eachcategorypages.models import Product
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q

from carts.views import _cart_id
from carts.models import Cart,CartItem



def home(request):
    products=Product.objects.all().filter(is_available=True).order_by('id')

    sort_by = request.GET.get('sort_by')
    if sort_by == 'name_a_to_z':
        products = products.order_by('product_name')
    elif sort_by == 'name_z_to_a':
        products = products.order_by('-product_name')
    elif sort_by == 'price_low_to_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_to_low':
        products = products.order_by('-price')
    

    paginator=Paginator(products,9)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    
    context={
        'products': paged_products,
        
        'home':carousel_Home.objects.all().order_by('id'),
        
        'banner':Banner.objects.all(),
    }

    return render(request,"home.html",context)






def login(request):
    if request.user.is_authenticated:
        return redirect(home)
    
    if request.method == 'POST':
       
        username=request.POST["username"]
        password=request.POST["password"]
        user=auth.authenticate(username=username,password=password)
        
        if user is not None:

            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user=user
                        item.save()

            except:
                pass    
              

            auth.login(request,user)
            return redirect(home)
            
        
        else:
            messages.info(request,"Invalid User")
            return redirect(login)
    else:
        return render(request,'login.html')





def signup(request, verify=None):
    usr = None
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        # OTP Verification
        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username=get_usr)
            try:
                if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                    usr.is_active = True
                    usr.save()
                    UserOTP.objects.filter(user=usr).delete()  # deleting otp after use
                    messages.success(request, 'Registration successful.')
                    return redirect(login)
                else:
                    messages.warning(request, 'You Entered a wrong OTP')
                    return render(request, 'signup.html', {'otp': True, 'usr': usr})
            except ValueError:
                messages.warning(request, 'Please enter only digits for OTP.')
                return render(request, 'signup.html', {'otp': True, 'usr': usr})

        else:
            
         name =request.POST['name']
         email =request.POST['email']
         password =request.POST['password1']
         password2 =request.POST['password2']
         if password==password2:
                        
                      if User.objects.filter(username=name).exists():
                         messages.info(request,'username is already exists')
                         return redirect(signup)

                      elif User.objects.filter(email=email).exists():
                        messages.info(request,'email is already exists')
                        return redirect(signup)

                      else:
                        usr=User.objects.create_user(username=name,password=password,email=email)
                        usr.set_password(password)
                        usr.is_active=False
                        usr.save()
                        usr_otp=random.randint(100000,999999)
                        UserOTP.objects.create(user=usr,otp=usr_otp)
                        mess=f'Hello\t{usr.username},\nYour OTP to verify your account for INDRESS is {usr_otp}\nThanks!'
                        send_mail(
                                "welcome to INDRESS E-commerce-Verify your Email",
                            
                                mess,
                                settings.EMAIL_HOST_USER,
                                [usr.email],
                                fail_silently=False
                            )
                        return render(request,'otp.html',{'otp':True,'usr':usr})
         else:
            messages.info(request,'password does not exists')
            return redirect(signup)
    

    else:
        return render(request,'signup.html')





   


def logout(request):
    auth.logout(request)
    return redirect(login)


def otp(request):
    return render(request,'otp.html')  


def product_details_view(request,dress_id):
    
   
    return render(request,'product_details_view.html')




def search(request):
    products=''
    product_count=0

    if 'keyword' in request.GET:
        keyword=request.GET['keyword']

        if keyword:
            products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword) )
            product_count=products.count()
    context={
        'products':products,
        'product_count':product_count
        
     }    

    return render(request,'home.html',context)



#========== errors==============
def error_404(request,exception):
    return render(request,'404.html')































