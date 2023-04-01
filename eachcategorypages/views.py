from django.shortcuts import render,redirect,get_object_or_404
from .models import carousel_Men,carousel_Women,carousel_Kid
from eachcategorypages.models import Product,ProImage
from eachcategorypages.models import Category
from carts.views import _cart_id
from carts.models import CartItem

# from wishlist.views import _wishlist_id
# from wishlist.models import WishlistItem, Wishlist

from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.contrib import messages
from .forms import ReviewForm
from .models import ReviewRating


# Create your views here.

def men(request,category_slug=None):
    categories=None
    products=None

    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
        paginator=Paginator(products,4)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
    
    else:
         products=Product.objects.all().filter(is_available=True)
         paginator=Paginator(products,4)
         page=request.GET.get('page')
         paged_products=paginator.get_page(page)
         product_count=products.count()


    
   
    
    men=carousel_Men.objects.all()
    
    context={
        'products':paged_products,
        'men':men,
        'product_count':product_count,
    }
    return render(request,'men.html',context)


def women(request):
    products=Product.objects.all().filter(is_available=True)
    product_count=products.count()
    women=carousel_Women.objects.all()

    context={
        'products':products,
        'women':women,
        'product_count':product_count,
    }
    
    return render(request,'women.html',context)



def kids(request):
    dict_kids={
        'kids':carousel_Kid.objects.all()
    }
    return render(request,'kids.html',dict_kids)    






def product_detail(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        # wishlist_instance = Wishlist.objects.get(wishlist_id =_wishlist_id(request) )
        # in_wishlist=WishlistItem.objects.filter(wishlist = wishlist_instance,product=single_product).exists()
    
    except Exception as e:
        raise e
    print(single_product)
    products=ProImage.objects.filter(product=single_product)
    
    #review only  for the purchased customers
    # try:
    #     orderproduct = OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists
    # except OrderProduct.DoesNotExist:
    #     orderproduct = None    

    #to get all the users reviews.
    reviews=ReviewRating.objects.filter(product_id=single_product.id,status=True)

    context={
        'single_product': single_product ,
        'in_cart':in_cart,
        'products':products,
        # 'in_wislist':in_wishlist,
        
        # 'orderproduct':orderproduct,

        'reviews':reviews,
    }


    return render(request,'product_detail.html',context)




# def submit_review(request,product_id):
#     url=request.META.get('HTTP_REFERER')
#     if request.method == 'POST':
#         try:
#             review=ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
#             form=ReviewForm(request.POST,instance=review)
#             form.save()
#             messages.success(request,'Thank you! Your review has been updated.')
#             return redirect(url)

#         except ReviewRating.DoesNotExist:
#             form=ReviewForm(request.POST)
#             if form.is_valid():
#                 data=ReviewRating()
#                 data.subject=form.cleaned_data['subject']
#                 data.rating=form.cleaned_data['rating']
#                 data.review=form.cleaned_data['review']
#                 data.ip=request.META.get('REMOTE_ADDR') 
#                 data.product_id=product_id
#                 data.user_id=request.user.id
#                 data.save()
#                 messages.success(request,'Thank you! Your review has been submitted.')
#                 return redirect(url)


                 


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
