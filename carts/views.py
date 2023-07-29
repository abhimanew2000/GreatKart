from django.shortcuts import render, redirect,get_object_or_404
from app.models import Product
from .models import Carts, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from app.models import Variation
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    if request.method=="POST":
        for item in request.POST:
            key = item
            value=request.POST[key]
            try:
                variations=Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                print(variations)
            except:
                pass

    product = Product.objects.get(id=product_id)
    try:
        cart = Carts.objects.get(cart_id=_cart_id(request))
    except Carts.DoesNotExist:
        cart = Carts.objects.create(cart_id=_cart_id(request))

    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()

    return redirect('cart')

def remove_cart(request,product_id):
    cart=Carts.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)  # Correct the variable name here
    cart_item= CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Carts.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    
    try:
        
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')


def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grandtotal=0
        cart = Carts.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
       
        for cart_item in cart_items:
            total += cart_item.product.marked_price * cart_item.quantity
            quantity += cart_item.quantity
            cart_item.ram_variations = cart_item.product.variation_set.filter(variation_category='ram', is_active=True)
            cart_item.size_variations = cart_item.product.variation_set.filter(variation_category='size', is_active=True)
        tax=(2* total)/100
        grandtotal =total+ tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax':tax,
        'grandtotal':grandtotal,
    }
    return render(request, 'store/cart.html', context)

