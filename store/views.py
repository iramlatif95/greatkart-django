from django.shortcuts import render,get_object_or_404
from .models import Product 
from category.models import Category
from carts.views import _cart_id
from carts.views import CartItem
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from django.db.models import Q # this for the or query
# This is a test change




    

"""def home(request):
     
    products=Product.objects.all().filter(is_available=True) # only filter that produt that is the available 

   
    context={
        'products':products
        

    }
    return render(request,'home.html',context)"""
    
    
   

# for the store .html
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)# only shows that products that is the available 
        paginator=Paginator(products,2)
        page=request.GET.get('page') # page=2
        paged_products=paginator.get_page(page)
        product_count = products.count() # this is used to count the the how many products are in a browser 
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator=Paginator(products,4)
        page=request.GET.get('page') # page=2
        paged_products=paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)

# produt detail 
def product_detail(request,category_slug,product_slug):

    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists
    except Exception as e:
        raise e 
    context={
        'single_product':single_product,
        'in_cart':in_cart,

    }

    return render(request,'product_detail.html',context)

# this is the for the search 
def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.filter (Q(description__icontains=keyword) | Q(product_name__icontains=keyword)) # search as the deso or the product name
            product_count = products.count()
            context={
                'products':products,
                'product_count':product_count,
            }
    return render(request, 'store.html',context)
