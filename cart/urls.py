from django.urls import path, include
from . import views

urlpatterns = [
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('cart/', views.cart, name='cart'),
]
