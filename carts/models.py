from django.db import models
from app.models import Product,Variation,User
# Create your models here.
class Carts(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation=models.ManyToManyField(Variation,blank=True)
    cart = models.ForeignKey(Carts,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.selling_price * self.quantity
    
    def get_ram_variations(self):
        return self.variation.filter(variation_category='ram', is_active=True)

    def get_size_variations(self):
        return self.variation.filter(variation_category='size', is_active=True)

    def __unicode__(self) :
        return str(self.product)
