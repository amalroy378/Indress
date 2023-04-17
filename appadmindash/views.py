from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from eachcategorypages.models import Product,Category
from django.shortcuts import get_object_or_404


from django.contrib import messages
from app.models import dress,carousel_Home
from orders.models import Order,OrderProduct
from django.db.models import Sum

import matplotlib.pyplot as plt
from django.http import HttpResponse
from io import BytesIO
from django.contrib.auth.decorators import login_required



# Create your views here.

def adminlogin(request):
    
    if request.method == 'POST':
       
        username=request.POST["username"]
        password=request.POST["password"]
        user=auth.authenticate(username=username,password=password)
        if user is not None:
           
            if user.is_superuser:
                return redirect(productlist)
            else:
                messages.info(request,"Invalid User")
                return redirect(adminlogin)        
        
        else:
            messages.info(request,"Invalid User")
            return redirect(adminlogin)
    else:
        return render(request,'adminlogin.html')

def index(request):

    return render(request,"index.html")


@login_required(login_url='login')
def productlist(request):
    if request.method == 'POST':
        search_text = 'etd'
        context = {
            'products':Product.objects.filter(product_name__icontains=search_text),
            'category':Category.objects.all(),
            
        }
    else:
        context = {
            'products':Product.objects.all().order_by('id'),
            'categories':Category.objects.all(),
            
        }
    return render(request,"productlist.html",context)    




       

def product_delete(request,product_id):
    del_product = Product.objects.filter(id=product_id)
    del_product.delete()
    return redirect(productlist)




def edit_product(request,product_id):
    name = request.POST['product_name']
    price = request.POST['product_price']
    # stock = request.POST['product_stock']
    category = request.POST['product_category']

    try:
        product = Product.objects.get(id=product_id)
        image = request.FILES['image']
        product.images=image
        product.save()
    except:
        pass    

    category_instance = Category.objects.get(id=category)
    product = Product.objects.filter(id=product_id).update(product_name=name,category=category_instance,price=price)
    mess_status = True
    return redirect(productlist)






def add_product(request):
    name = request.POST['product_name']
    category = request.POST['product_category']
    price = request.POST['product_price']
    stock = request.POST['product_stock']
    image = request.FILES['image']
    category_instance = Category.objects.get(id=category)
    new = Product.objects.create(is_available=True,images=image,product_name=name,category=category_instance,price=price,stock=stock)
    new.save()


    return redirect(productlist)




@login_required(login_url='login')
def userlist(request):
    dict_user={
        'user':User.objects.all().order_by('id')
    }
    
    return render(request,'userlist.html',dict_user)




def block_unblock(request,id):
    user = get_object_or_404(User,id=id)
    if user.is_active:
        user.is_active = False
        user.save()
        return redirect(userlist)
    else:
        user.is_active = True
        user.save()
        return redirect(userlist)


@login_required(login_url='login')
def categorylist(request):
    dict_category = {
        'categories':Category.objects.all().order_by('id')
    }
    return render(request,'categorylist.html',dict_category)

def add_category(request):
    try:
        image = request.FILES['image']
    except:
        pass
    name = request.POST['category_name']

    Category.objects.create(category_name=name,cat_image=image).save()
    return redirect(categorylist)

def edit_category(request,category_id):
    try:
        category = Category.objects.get(id=category_id)
        image = request.FILES['image']
        category.cat_image = image
        category.save()
    except:
        pass
    name = request.POST['category_name']
    category = Category.objects.filter(id=category_id)
    category.update(category_name=name)
    return redirect(categorylist)

def delete_category(request,category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect(categorylist)


@login_required(login_url='login')
def usermanagement(request):
    return render(request,"usermanagement.html") 

@login_required(login_url='login')
def dashboard(request):
    product_count=Product.objects.all()
    product_count=product_count.count()
    
    user_count=User.objects.all()
    user_count=user_count.count()

     
    order_count=User.objects.all()
    order_count=order_count.count()


    product_price = OrderProduct.objects.aggregate(Sum('product_price'))['product_price__sum']

    # product_price = round( product_price, 2)

    order =Order.objects.all()
    product=Product.objects.all()


    context={
       'product_count':product_count,
       'user_count':user_count,
       'order_count':order_count,
       'product_pric': product_price,
       'order':order,
       'product':product



    }
    return render(request,'dashboard.html',context)






@login_required(login_url='login')
def my_bar_chart_view(request):
    # Sample data

    products_1000 = Product.objects.filter(price__range=(1, 999))
    count = 0
    for product in products_1000:
        count+=1

    products_1000_2000 = Product.objects.filter(price__range=(1000, 1999))
    count1 = 0
    for product in products_1000_2000:
        count1+=1

    products_2000_3000 = Product.objects.filter(price__range=(2000, 2999))
    count2 = 0
    for product in products_2000_3000:
        count2+=1

    products_3000_4000 = Product.objects.filter(price__range=(3000, 4000))
    count3 = 0
    for product in products_3000_4000:
        count3+=1



    x_values = ['1000', '2000', '3000', '4000']
    y_values = [count, count1, count2, count3]

    # Create bar chart
    plt.bar(x_values, y_values)

    # Set title and labels for x and y axis
    plt.title("Bar Chart")
    plt.xlabel("Price")
    plt.ylabel("Number of Products")

    # Save the chart as a PNG file
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Serve the file as a HTTP response
    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="my_bar_chart.png"'
    return response




# def sales_report(request):  


#     product=Product.objects.all()
    
#     context={
#         'product':product,
#     }

#     return render(request,'sales_report.html',context)


# def sales(request):
#     context = {}

#     if request.method == 'POST':

#         start_date = request.POST.get('start-date')
#         end_date = request.POST.get('end-date')

#         if start_date == '' or end_date == '':
#             messages.error(request,'Give date first')
#             return redirect(sales)

#         order_items = Pro.objects.filter(order_ordered_dategte=start_date, orderordered_date_lte=end_date)
#         if order_items:
#             print(order_items)
#             context.update(sales = order_items,s_date=start_date,e_date = end_date)
#         else:
#             messages.error(request,'no data found')


#     return render(request,'adminpanel/sales_report.html',context)



@login_required(login_url='login')
def banner_management(request):
    
    context={
        'carousel':carousel_Home.objects.all().order_by('id'),
    }
    
    return render(request,'banner_management.html',context)



def banner_delete(request,carousel_id):
    del_banner = carousel_Home.objects.filter(id=carousel_id)
    del_banner.delete()
    return redirect(banner_management)



def banner_add(request):
    print('TEXT ===============  ',request.POST['carousel_text'])
    IMG = request.FILES['carousel_img']
    carousel_text = request.POST['carousel_text']
    new = carousel_Home.objects.create(carousel_img=IMG,carousel_text=carousel_text)
    new.save()


    return redirect(banner_management)
