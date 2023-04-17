from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import User

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Email address is required')

        if not username:
            raise ValueError('Username is required')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
           
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    


    # Required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
 
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True



class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    state = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    house_name = models.CharField(max_length=150)
    delivery_instruction = models.CharField(max_length=150)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name='Address'
        verbose_name_plural='Addresses'
        
        
class User_Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    img=models.ImageField(upload_to='profile_image')        