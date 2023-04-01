from django.urls import path
from . views import *

urlpatterns = [
  path('men/',men,name='men'),
  path('women/',women,name='women'),
  path('kids/',kids,name='kids'),

  path('category/<slug:category_slug>/',men, name='products_by_category'),
  path('category/<slug:category_slug>/<slug:product_slug>/',product_detail,name='product_detail'),
  
  path('submit_review/<int:product_id>/',submit_review,name='submit_review'),
 

]


