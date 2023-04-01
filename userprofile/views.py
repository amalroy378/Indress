from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import Account,Address
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.urls import reverse
from .forms import UserAddressForm


# Create your views here.
def user_profile(request):
    context = {
        'user_addresses': Address.objects.filter(user=request.user)
    }
    return render(request,'user_profile.html',context)





def edit_profile(request, user_id):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        print(user_id)
        edited_user = User.objects.filter(id=user_id)
        print(edited_user)
        edited_user.update(username=username)
        messages.success(request,'Profile Details updated successfully')
        return redirect('user_profile')
    
    return render(request, 'edit_profile.html')



def change_password(request, user_id):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        user = User.objects.get(id=user_id)
        if not user.check_password(old_password):
            messages.error(request, 'Incorrect password')
            return redirect(user_profile)
        else:
            if new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                messages.success(request, 'Password changed succesfully!')
                return redirect(user_profile)
            else:
                messages.error(request, 'Password doesnot match.')
                return redirect(user_profile)
            
    return render(request,'change_password.html')
        


def view_address(request):
     addresses = Address.objects.filter(full_name=request.user)
     print(addresses)
     context = {
          'addresses': addresses,
     }
     return render(request,"user_profile.html",context)


def add_address(request):
     if request.method == "POST":
          address_form = UserAddressForm(data=request.POST)
          if address_form.is_valid():
               
               address = address_form.save(commit=False)
               address.user = request.user
               address.save()  
               return redirect(user_profile)
     else:
         
          address_form = UserAddressForm()
     return render(request,"address.html",{"form": address_form})




def edit_address(request,id,num):
     if request.method == "POST":
          address=Address.objects.get(pk=id,user=request.user)
          address_form = UserAddressForm(instance = address,data=request.POST)
          if address_form.is_valid():
               address_form = address_form.save(commit=False)
               address_form.customer = request.user
               address_form.save()
               if num ==1:
                    return HttpResponseRedirect(reverse("user_profile"))
               elif num ==2:
                    return HttpResponseRedirect(reverse('checkout'))
     else:
          address=Address.objects.get(pk=id,user=request.user)
          address_form = UserAddressForm(instance = address)
     return render(request,"address.html",{"form": address_form})

             
def delete_address(request,id,nam):
    address=Address.objects.get(pk=id,user=request.user)
    address.delete()
    if nam == 1:
         return redirect('user_profile')
    elif nam == 2:
         return redirect('checkout')

      
def default_address(request,id,new):
    Address.objects.filter(user=request.user,default=True).update(default=False)
    Address.objects.filter(pk=id,user=request.user).update(default=True)
    if new == 1:
         return redirect('user_profile')
    elif new == 2:
         return redirect('checkout')

