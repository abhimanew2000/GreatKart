from django.contrib import admin
from app.models import Product,Cart,wishlist,CartProduct,Category,Order
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(Category)
