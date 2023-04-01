from django.urls import path
from . views import *

urlpatterns = [
    path('cart/',cart,name='cart'),
    path('add_cart/<int:product_id>/',add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/',remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:product_id>/',remove_cart_item,name='remove_cart_item'),
    
    path('checkout/',checkout,name='checkout'),
    path('success_page/',success_page,name='success_page'),

    path('cod/',cod,name='cod'),







]