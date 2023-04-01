from django.db import models
from django.urls import reverse
from userprofile.models import Account
from django.contrib.auth.models import User
from django.db.models import Avg


# Create your models here.


class carousel_Men(models.Model):
    carousel_img  =models.ImageField(upload_to='carousel_photos')
    carousel_text =models.CharField(max_length=200)


    def __str__(self):
        return self.carousel_text
    

class carousel_Women(models.Model):
    carousel_img  =models.ImageField(upload_to='carousel_photos')
    carousel_text =models.CharField(max_length=200)


    def __str__(self):
        return self.carousel_text


class carousel_Kid(models.Model):
    carousel_img  =models.ImageField(upload_to='carousel_photos')
    carousel_text =models.CharField(max_length=200)


    def __str__(self):
        return self.carousel_text
        


class MenTopWear(models.Model) :
    topwear_img         =models.ImageField(upload_to='topwear_images')       
    topwear_brand       =models.CharField(max_length=200)
    topwear_description =models.CharField(max_length=200)

    def __str__(self):
        return self.topwear_brand
        

class Category(models.Model):
    category_name   =models.CharField(max_length=100,unique=True)
    slug            =models.SlugField(max_length=100,unique=True)
    description     =models.TextField(max_length=200,blank=True)
    cat_image       =models.ImageField(upload_to='categories',blank=True)

    class Meta:
        verbose_name       ='category'
        verbose_name_plural='categories'


    def get_url(self):
            return reverse("products_by_category",args=[self.slug])

    def __str__(self):
        return self.category_name





# class Brand(models.Model):
#     brand_name    =models.CharField(max_length=100)
#     slug          =models.SlugField(max_length=200,unique=True)

#     def __str__(self):
#         return self.brand_name


 

class Product(models.Model):
    product_name  =models.CharField(max_length=200)
    slug          =models.SlugField(max_length=200,unique=True,null=True,blank=True)
    description   =models.TextField(max_length=500)
    price         =models.IntegerField()
    images        =models.ImageField(upload_to="products")
    stock         =models.IntegerField()
    is_available  =models.BooleanField(default=True)
    category      =models.ForeignKey(Category,on_delete=models.CASCADE)
    # brand         =models.ForeignKey(Brand,on_delete=models.CASCADE)
    created_date  =models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)


    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])

    def __str__(self): 
        return self.product_name
    
    def averageReview(self):
        reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg=float(reviews['average'])
        return avg    




class ProImage(models.Model):
    product  =  models.ForeignKey(Product,on_delete=models.CASCADE,related_name='image')
    image    =  models.ImageField(upload_to='img' ,default="",null=True,blank=True)

    def __str__(self): 
        return f'{self.product.product_name}'
    



class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


 



     
