from .models import Cart,CartItem


def counter(request):
    cart_count=0
    if request.user.is_authenticated:
        if 'admin' in request.path:
            return {}
        
        else:
            try:
                # current_cart=Cart.objects.get(user=request.user,is_active =True)
                current_cart = Cart.objects.filter(user=request.user, is_active=True).order_by('-date_added').first()

                print('cart = ',current_cart)
                if current_cart:
                    items=CartItem.objects.filter(cart=current_cart)
                
                    for item in items:
                        cart_count+=item.quantity

            except Cart.DoesNotExist:
                item=0       

    return dict(cart_count=cart_count)