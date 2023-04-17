from django.urls import path
from . import  views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('order_show/',views.order_show,name='order_show'),
    
    path('remove_cart_item/<int:product_id>/',views.remove_cart_item,name='remove_cart_item'),
    
    



]
