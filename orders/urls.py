from django.urls import path
from . import  views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('order_show/',views.order_show,name='order_show'),



]
