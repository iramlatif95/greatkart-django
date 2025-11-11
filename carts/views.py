from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Variation
from . models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def _cart_id(request):  # _private function 
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # get the product 
    product_variation = []

    # Handle product variations from POST data
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # Get or create cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    # Check if cart item already exists
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        ex_var_list = []
        ids = []

        for item in cart_items:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            ids.append(item.id)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = ids[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            # Assign user if logged in
            if request.user.is_authenticated:
                item.user = request.user
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.add(*product_variation)
            if request.user.is_authenticated:
                item.user = request.user
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.add(*product_variation)
        if request.user.is_authenticated:
            cart_item.user = request.user
        cart_item.save()

    return redirect('cart')

# for the remove 
def remove_cart(request, product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')

# remove cart_item
def remove_cart_item(request, product_id,cart_item_id): # remove b
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id) 
    cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
    cart_item.delete()  
    return redirect('cart')

def cart(request,total=0,quantity=0,cart_item=None):
    tax=0
    grand_total=0
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
            tax=(2 * total)/100
            grand_total=total+tax

    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total': grand_total,
    }
    return render(request,'cart.html',context)

@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_item=None):
    tax=0
    grand_total=0
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
            tax=(2 * total)/100
            grand_total=total+tax

    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total': grand_total,
    }
    
    return render(request,'checkout.html',context)

# Create your views here.
