from django.shortcuts import render,redirect
from.forms import RegistrationForm
from.models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name'] # cleaned data in this is used to fetch data in form
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
            #create user
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password) # create user from model.py
            user.phone_number=phone_number
            user.is_active = True
            user.save()
            messages.success(request, 'successful regtster.')
            return redirect('login')
    else:
            form=RegistrationForm()
    context={
        'form':form,
    }
    return render(request,'register.html',context)


def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            #messages.success(request,'you are now loggin.')
            return redirect('home')
        else:
            messages.error(request,'invalid login credentials.')
            return redirect('login')
    return render(request,'login.html')
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are loged out')
    #return render(request,'logout.html')
    return redirect('login')


# Create your views here.
