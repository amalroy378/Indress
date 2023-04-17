from django.db import models
from eachcategorypages.models import Product
from app.models import Variation
from userprofile.models import Account
from django.contrib.auth.models import User
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    cart_id=models.CharField(max_length=235,blank=True)
    date_added=models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True,null=True)

    def __str__(self):
        return str(self.cart_id)
    


class CartItem(models.Model):

    user      =models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product   =models.ForeignKey(Product,on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variation,blank=True)
    color = models.CharField(null=True)
    size = models.CharField(null=True)
    cart      =models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity  =models.IntegerField()
    is_active =models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):      
        return str(Product.objects.get(id=self.product.id))


