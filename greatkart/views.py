

from django.shortcuts import render
from store.models import Product 



    

def home(request):
     
    products=Product.objects.all().filter(is_available=True) # only filter that produt that is the available 

   
    context={
        'products':products
        

    }
    return render(request,'home.html',context)
    
    