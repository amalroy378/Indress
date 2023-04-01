from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('wishlist/', wishlist, name='wishlist'),    
    path('add_wishlist/<int:product_id>/',add_wishlist, name='add_wishlist'),    
    path('remove_wishlistitem/<int:product_id>/' ,remove_wishlistitem, name='remove_wishlistitem'),    
         
]
