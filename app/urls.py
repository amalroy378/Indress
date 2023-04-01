from django.urls import path
from . views import *

urlpatterns = [
    path('',home,name='home'),
    path('login/',login,name='login'),
    path('signup/',signup,name='signup'),
    path('logout/',logout,name='logout'),
    path('otp/',otp,name='otp'),
    path('product_details_view/<int:dress_id>',product_details_view,name='product_details_view'),
    path('search/',search,name='search'),

    
]
