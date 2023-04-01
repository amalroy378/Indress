from django.db import models
from django.contrib.auth.models import User
from eachcategorypages.models import Product




# Create your models here.

class Profile(models.Model):
    user    =models.OneToOneField(User,on_delete=models.CASCADE)
    mobile  =models.CharField(max_length=10)
    otp     =models.CharField(max_length=6)



class dress(models.Model):
    dress_img  =models.ImageField(upload_to='photos')
    dress_name =models.CharField(max_length=200)
    


    
    

    def __str__(self):
        return self.dress_name 
    
        



class UserOTP(models.Model):
    user    =models.ForeignKey(User,on_delete=models.CASCADE)
    time_st =models.DateTimeField(auto_now=True)
    otp     =models.IntegerField()




class carousel_Home(models.Model):
    carousel_img  =models.ImageField(upload_to='home_photos')
    carousel_text =models.CharField(max_length=200)




variation_category_choice=(
    ('color','color'),
    ('size','size'),
)


class   VariationManager(models.Manager)  :
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)





class Variation(models.Model):
    product             =models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category  =models.CharField(max_length=100,choices=variation_category_choice)
    variation_value     =models.CharField(max_length=100)
    is_active           =models.BooleanField(default=True)
    created_date        =models.DateTimeField(auto_now=True)

    objects=VariationManager()

    def __unicode__(self):
        return self.product
    


class Banner(models.Model):
    banner_img  =models.ImageField(upload_to='banner_images')
    banner_text =models.CharField(max_length=200)





