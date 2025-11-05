from django.shortcuts import render
from.forms import RegistrationForm
from.models import Account

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
            user.save()
    else:
            form=RegistrationForm()
    context={
        'form':form,
    }
    return render(request,'register.html',context)


def login(request):
    return render(request,'login.html')

def logout(request):
    return render(request,'logout.html')


# Create your views here.
