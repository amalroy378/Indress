from django.urls import path
from . views import *

urlpatterns = [
    path('user_profile/',user_profile,name='user_profile'),

    path('edit_profile/<int:user_id>/', edit_profile, name="edit_profile"),
    path('change_password/<int:user_id>/',change_password, name="change_password"),

    path('addresses', view_address, name='addresses'),   
    path('add_address',add_address, name='add_address'),  

    path('addresses/edit_address/<int:id>/<int:num>/', edit_address, name='edit_address'),   
    path('addresses/delete_address/<int:id>/<int:nam>/', delete_address, name='delete_address'),   
    path('addresses/default_address/<int:id>/<int:new>/', default_address, name='default_address'),   
]