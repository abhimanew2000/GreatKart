from django.urls import path
from .import views

urlpatterns = [
    path("",views.cart,name='cart'),
    path("add_cart/<int:product_id>/",views.add_cart,name='add_cart'),
    path("remove_cart/<int:product_id>/<int:cart_item_id>/",views.remove_cart,name='remove_cart'),
    path("remove_cart_item/<int:product_id>/",views.remove_cart_item,name='remove_cart_item'),
    path("remove_cart_item/<int:product_id>,<int:cart_item_id>/",views.remove_cart_item,name='remove_cart_item'),
    # path("checkout_page/<int:grand_total>/",views.checkout_page,name='checkout_page'),
    path("checkout/<int:grandtotal>/",views.checkout,name='checkout'),

    # path('razorpay/<int:grandtotal>/', views.razorpay_view, name='razorpay'),
    # path('order_payment/', views.order_payment, name='order_payment'),

    # path('success/<int:id>/', views.success_view, name='success'),



    path('razorpaycheck', views.razorpaycheck,name='razorpaycheck',),
    path('myorders', views.myorders,name='myorders'),
    






]
