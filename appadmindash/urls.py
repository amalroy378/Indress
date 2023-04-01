from django.urls import path
from . views import *

urlpatterns = [
 path('adminlogin/',adminlogin,name='adminlogin'),
 path('index/',index,name='index'),
 path('productlist/',productlist,name='productlist'),
 path('usermanagement/',usermanagement,name='usermanagement'),
 path('delete_product/<int:product_id>',product_delete,name='delete_product'),
 path('edit/<int:product_id>',edit_product,name='edit_product'),
 path('add_product',add_product,name='add_product'),  
 path('userlist/',userlist,name='user_list'),
 path('block_unblock/<int:id>',block_unblock,name="block_unblock"),
 path('categorylist/',categorylist,name='categorylist'),
 
 path('delete_category/<int:category_id>',delete_category,name='delete_category'),
 path('edit_category/<int:category_id>',edit_category,name='edit_category'),
 path('add_category',add_category,name='add_category'),
 path('dashboard/',dashboard,name='dashboard'),

 path('my_bar_chart_view/',my_bar_chart_view,name='my_bar_chart_view'),
#  path('sales/',sales,name='sales')




]
