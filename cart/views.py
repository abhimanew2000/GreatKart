from django.shortcuts import render, redirect
from app.models import Product, Cart, CartProduct

def _cart_id(request):
    cart = request.session.get('cart_id')
    if not cart:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_id = _cart_id(request)

    try:
        cart_product = CartProduct.objects.get(cart_id=cart_id, product=product)
        cart_product.quantity += 1
        cart_product.save()
    except CartProduct.DoesNotExist:
        cart_product = CartProduct.objects.create(
            cart_id=cart_id,
            product=product,
            rate=product.selling_price,
            quantity=1,
            subtotal=product.selling_price,
        )

    return redirect('cart')

def cart(request):
    cart_id = _cart_id(request)
    cart_products = CartProduct.objects.filter(cart_id=cart_id)
    total_price = sum(cp.subtotal for cp in cart_products)

    context = {
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'store/cart.html', context)
