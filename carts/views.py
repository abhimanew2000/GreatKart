from django.shortcuts import render, redirect,get_object_or_404
from app.models import Product
from .models import Carts, CartItem
from django.core.exceptions import ObjectDoesNotExist
from app.models import Variation
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from userauths.models import Address
from orders.models import Order,OrderProduct,Payment
import razorpay
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
import hmac
import hashlib
import logging
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user=request.user
    product = Product.objects.get(id=product_id)
    # if user is authenticated
    if current_user.is_authenticated:
        product_variation=[]
        if request.method=="POST":
            for item in request.POST:
                key = item
                value=request.POST[key]
            try:
                variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                print(variation)
                product_variation.append(variation)
            except:
                pass

        
        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,user=current_user)
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)
            if product_variation in ex_var_list:
                # increase cartitem quantity
                index=ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity +=1
                item.save()
            else:
                # create new cartitem
                item=CartItem.objects.create(product=product,quantity=1,user=current_user)
                if len(product_variation) >0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
            # cart_item.quantity +=1
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            

            if len(product_variation) >0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
                cart_item.save()
        
        return redirect('cart')
    #if user is not authenticated 
    else:
        product_variation=[]
        if request.method=="POST":
            for item in request.POST:
                key = item
                value=request.POST[key]
            try:
                variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                print(variation)
                product_variation.append(variation)
            except:
                pass

        try:
            cart = Carts.objects.get(cart_id=_cart_id(request))
        except Carts.DoesNotExist:
            cart = Carts.objects.create(cart_id=_cart_id(request))

        cart.save()
        is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()


        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,cart=cart)

            # existing variations---datatbse
            # Current variation---->produt_variation
            # item_id---
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)
            if product_variation in ex_var_list:
                # increase cartitem quantity
                index=ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity +=1
                item.save()


            else:
                # create new cartitem
                item=CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation) >0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
            # cart_item.quantity +=1
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            

            if len(product_variation) >0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
                cart_item.save()
        
        return redirect('cart')

    
    # if request.method=="POST":
    #     varient=request.POST.get('size')
    #     print('varient=',varient) 
    #     # for item in request.POST:
    #     #     key = item
    #     #     value=request.POST[key]
    #     #     print('key'+key)
    #     #     print('value'+value)
    #     try:
    #         variations=Variation.objects.get(product=product,variation_value=varient)
    #         print('varientssss=',variations)
    #     except :
    #         pass

    # try:
    #     cart = Carts.objects.get(cart_id=_cart_id(request))
    # except Carts.DoesNotExist:
    #     cart = Carts.objects.create(cart_id=_cart_id(request))

    # cart.save()
    

    # try:
    #     cart_item = CartItem.objects.get(product=product, cart=cart)
    #     cart_item.quantity += 1
    #     cart_item.save()
    # except CartItem.DoesNotExist:
    #     cart_item = CartItem.objects.create(
    #         product=product,
    #         quantity=1,
    #         cart=cart,
    #     )
    #     if varient:
    #         cart_item.variation.set([variations])    
    #     cart_item.save()

    # return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    product=get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
            cart=Carts.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity >1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')
    
    # cart=Carts.objects.get(cart_id=_cart_id(request))
    # product = get_object_or_404(Product, id=product_id) 
    #  # Correct the variable name here
    # cart_item= CartItem.objects.get(product=product,cart=cart)
    # if cart_item.quantity >1:
    #     cart_item.quantity -=1
    #     cart_item.save()
    # else:
    #     cart_item.delete()
    
    # return redirect('cart')
# remove button 
def remove_cart_item(request, product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
    else:
        cart=Carts.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
    # product = get_object_or_404(Product, id=product_id)
    # if request.user.is_authenticated:
    #     cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    # else:
    #     cart = Carts.objects.get(cart_id=_cart_id(request))
    #     cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    # cart_item.delete()
    # return redirect('cart')

def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grandtotal=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Carts.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.selling_price*cart_item.quantity)
            quantity += cart_item.quantity
        tax=(2* total)/100
        grandtotal =total+ tax
    except ObjectDoesNotExist:
        pass

    # try:
    #     tax=0
    #     grandtotal=0
    #     if request.user.is_authenticated:
    #         cart_items=CartItem.objects.filter(user=request.user,is_active=True)
    #         print(cart)
    #     else:
    #         cart = Carts.objects.get(cart_id=_cart_id(request))
    #         cart_items = CartItem.objects.filter(cart=cart, is_active=True)
       
    #     for cart_item in cart_items:
    #         print('varient=',cart_item.variation)
    #         total += cart_item.product.marked_price * cart_item.quantity
    #         quantity += cart_item.quantity
            
    #     tax=(2* total)/100
    #     grandtotal =total+ tax
        
    # except ObjectDoesNotExist:
    #     pass
    

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax':tax,
        'grandtotal':int(grandtotal),
    }
    print(context,"22222222222")
    return render(request, 'store/cart.html', context)


RAZORPAY_KEY_ID = 'rzp_test_4o90y50Nv7s1jR'
RAZORPAY_KEY_SECRET = 'nlmYaIYmAyx29rc3BUZSmDRu'

@login_required(login_url='handlelogin')
def checkout(request,grandtotal,total=0,quantity=0,cart_items=None,):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user, is_active=True)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    print(grandtotal)

    grand_total = grandtotal
    for cart_item in cart_items:
        print(cart_item.quantity)
        print(cart_item.product.selling_price)

        grand_total += cart_item.product.selling_price* cart_item.quantity
    tax = (2 * grand_total) / 100
    grand_total += tax
    print('grand_total',grand_total)
    addresses = Address.objects.filter(user=current_user)

    

    if request.method == 'POST':      
        selected_address_id = request.POST.get('selected_address')
        payment_id=request.POST.get('payment_id')
        print('paymentid',payment_id)
        print('selected address is :', selected_address_id) 
        # grand_total = int(request.POST.get('grand_total', 0))
        try:
            selected_address = Address.objects.get(pk=int(selected_address_id), user=request.user)
        except Address.DoesNotExist:
            return redirect('store')  # Redirect to store page if selected address is not found

        # Create the order
        order = Order.objects.create(
            user=request.user,
            tax=tax,
            selected_address=selected_address,
            order_total=grandtotal,
            status='New',  # Set the status to 'New' for a new order
            
        )
        for cart_item in cart_items:
            for variation in cart_item.variation.all():  # Loop through all variations for this cart item
                OrderProduct.objects.create(
                        order=order,
                        user=current_user,
                        product=cart_item.product,
                        variation=variation,  # Assign the specific variation
                        quantity=cart_item.quantity,
                        product_price=cart_item.product.selling_price,
                    )
            cart_item.product.view_count -= cart_item.quantity
            cart_item.product.save()

        cart_items.delete()

        # Here you can add additional logic to handle the cart items and payment
        payMode=request.POST.get('payment_method')
        if payMode=="razorpay":
            return JsonResponse({'status':"Order Placed successfully"})
        return redirect('order_success',id=order.id)  # Redirect to a success page after placing the order
    
    
    # order_id = create_razorpay_order(grandtotal)
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax':tax,
        'grandtotal':int(grandtotal),
        'addresses': addresses,
        # 'order_id': order_id,
    }
    

    return render(request,'store/checkout.html',context)


def success_view(request):
    order_id = request.session.get('order_id')  # Change this based on your logic
    order = get_object_or_404(Order, id=order_id)
    order_products = OrderProduct.objects.filter(order=order)

    context = {
        'order': order,
        'order_products': order_products,
    }
    return render(request, 'store/success.html')
import razorpay
import logging





@login_required
def razorpaycheck(request):
    current_user = request.user
    cart_items= CartItem.objects.filter(user=current_user)
    total_price=0
    for item in cart_items:
        total_price = total_price + item.product.selling_price * item.quantity
    tax = (2 * total_price) / 100
    total_price+=tax

    return JsonResponse({
        'total_price':int(total_price),

    })
def myorders(request):
    return HttpResponse("my orders page")


