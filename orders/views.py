from django.shortcuts import render,redirect
from carts.models import CartItem
from.models import Order,OrderProduct
import datetime
from django.contrib import messages
from userauths.models import Address
from django.shortcuts import get_object_or_404

# Create your views here.





# def place_order(request, total=0,quantity=0):
#     current_user=request.user
#     # if cartcount is lessthan = 0.hen rediresct to storepage
#     cart_items=CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()
#     if cart_count <= 0:
#         return redirect('store')
#     grand_total=0
#     tax=0
#     for cart_item in cart_items:
#         total +=(cart_item.product.selling_price * cart_item.quantity)
#         quantity += cart_item.quantity
#     tax=(2* total)/100
#     grand_total = total + tax
#     if request.method =="POST":
#         form= OrderForm(request.POST)
#         if form.is_valid():
#             # if form is valid store all details
#             data = Order()
#             data.first_name=form.cleaned_data['first_name']
#             data.last_name=form.cleaned_data['last_name']
#             data.phone=form.cleaned_data['phone']
#             data.email=form.cleaned_data['email']
#             data.address_line_1=form.cleaned_data['address_line_1']
#             data.address_line_2=form.cleaned_data['address_line_2']
#             data.country=form.cleaned_data['country']
#             data.state=form.cleaned_data['state']
#             data.city=form.cleaned_data['city']
#             data.order_note=form.cleaned_data['order_note']
#             data.order_total=grand_total
#             data.tax=tax
#             data.ip = request.META.get('REMOTE_ADDR') 
#             # this will give user ip
#             data.save()
#             # generate order numberby year date month
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr,mt,dt)
#             current_date= d.strftime("%Y%m%d")  
#             order_number= current_date + str(data.id)
#             data .order_number = order_number
#             data.save()
#             cart_items.delete()
#             messages.success(request, 'Order placed successfully!')

#             # Redirect the user back to the cart page
#             return redirect('cart') 
#          # Replace 'cart' with the URL name of your cart page
#         addresses = Address.objects.filter(user=current_user)

#     else:
#         form = OrderForm()
#     context = {
#         'form': form,
#         'cart_items': cart_items,
#         'total': total,
#         'quantity': quantity,
#         'grand_total': grand_total,
#         'addresses': addresses,
#     }

#     return render(request, 'store/checkout.html', context)


# def place_order(request, total=0,quantity=0):
#     current_user=request.user
#     # if cartcount is lessthan = 0.hen rediresct to storepage
#     cart_items=CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()
#     if cart_count <= 0:
#         return redirect('store')
#     grand_total=0
#     tax=0
#     for cart_item in cart_items:
#         total +=(cart_item.product.selling_price * cart_item.quantity)
#         quantity += cart_item.quantity
#     tax=(2* total)/100
#     grand_total = total + tax
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # If form is valid, get the selected address from the POST request data
#             selected_address_id = request.POST.get('selected_address')
#             selected_address = Address.objects.get_or_none(id=selected_address_id)

#             # If the selected address is not None, create an order with the selected address
#             if selected_address is not None:
#                 data = Order()
#                 data.first_name=form.cleaned_data['first_name']
#                 data.last_name=form.cleaned_data['last_name']
#                 data.phone=form.cleaned_data['phone']
#                 data.email=form.cleaned_data['email']
#                 # Use the selected address for the order
#                 user_addresses = Address.objects.filter(user=current_user)
#                 data.shipping_address = selected_address
#                 data.order_note=form.cleaned_data['order_note']
#                 data.order_total=grand_total
#                 data.tax=tax
#                 data.ip = request.META.get('REMOTE_ADDR') 
#                 # this will give user ip
#                 data.save()
#                 # generate order numberby year date month
#                 yr = int(datetime.date.today().strftime('%Y'))
#                 dt = int(datetime.date.today().strftime('%d'))
#                 mt = int(datetime.date.today().strftime('%m'))
#                 d = datetime.date(yr,mt,dt)
#                 current_date= d.strftime("%Y%m%d")  
#                 order_number= current_date + str(data.id)
#                 data .order_number = order_number
#                 data.save()
#                 cart_items.delete()
#                 messages.success(request, 'Order placed successfully!')

#                 # Redirect the user back to the cart page
#                 return redirect('cart') 
#          # Replace 'cart' with the URL name of your cart page
#             else:
#                 messages.error(request, 'Please select an address to place your order.')
            
#         else:
#             form = OrderForm()
#     else:
#         form = OrderForm()
#         user_addresses = Address.objects.filter(user=current_user)
#     context = {
#         'form': form,
#         'cart_items': cart_items,
#         'total': total,
#         'quantity': quantity,
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/checkout.html', context)










def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    context = {
        'orders': orders
    }
    return render(request, 'userauth/dashboard.html', context)
def order_success(request,id):
    order = get_object_or_404(Order,id=id,user=request.user)
    order_products = OrderProduct.objects.filter(order=order)
    print(f"Order ID: {order.id}")
    print(f"Order Total: {order.order_total}")
    print(f"Number of Order Products: {order_products.count()}")
    print(f"Order Products: {order_products}")
    context = {
        'order': [order],
        'order_products': order_products,
    }
    return render(request, 'store/order_success.html',context)
