from django.db import models
from userauths.models import User
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class VariationManager(models.Manager):
    
    def ramsize(self):
        return super(VariationManager,self).filter(variation_category='ram,size',is_active=True)

class Category(models.Model):
    title = models.CharField(max_length=200)
    cat_slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title
    def get_url(self):
        return reverse("products_by_category",args=[self.cat_slug])
        
    
    def save(self, *args, **kwargs):
        # Prepopulate the slug if it's not set
        if not self.cat_slug:
            self.cat_slug = slugify(self.title)  # Generate the slug from the title
        super().save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products", blank=True, null=True)
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    view_count = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        # Prepopulate the slug if it's not set
        if not self.slug:
            self.slug = slugify(self.title)  # Generate the slug from the title
        super().save(*args, **kwargs)
    def get_url(self):
        return reverse("products_detail",args=[self.category.cat_slug,self.slug])

variation_category_choice=(
    ('ram,size','ram,size'),
) 


class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)

    objects=VariationManager()

    def __str__(self) :
        return self.variation_value


    
    

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart {self.cart.id} - CartProduct {self.id}"


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the Way", "On the Way"),
    ("Order Completed", "Order Completed"),
    ("Order Cancelled", "Order Cancelled"),
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=200, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
class wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)


class ProductGallery(models.Model):
    product=models.ForeignKey(Product,default=None,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='products',max_length=255)

    def __str__(self) :
        return self.product.title
    class Meta:
        verbose_name="productgallery"
        verbose_name_plural="productgallery"