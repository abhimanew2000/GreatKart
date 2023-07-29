from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from userauths.models import User
from app.models import Category,Product

# Create your views here.

def admin_panel(request):
    return render(request, 'adminauth/admin_panel.html')

def admin_signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("email:",email,"password:",password)
        user = authenticate(request, email=email, password=password)
        if user and user.is_superuser:
            print("its superuser")
            login(request, user)
            return redirect('admin_panel')
            
    return render(request, 'adminauth/adminsignin.html')  
    

def userinfo(request):
    users = User.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        user = User.objects.get(id=user_id)

        if action == 'block':
            user.is_blocked = True
            user.save()
        elif action == 'unblock':
            user.is_blocked = False
            user.save()
    context = {
        'users': users,
    }
    return render(request,'adminauth/userinfo.html',context)

def categorylist(request):
    categories=Category.objects.all()

    return render(request,'adminauth/categorylist.html')
def productlist(request):
    products=Product.objects.all()
    context={
        'products':products,
    }
    return render(request,'adminauth/productlist.html',context)

def add_category(request):
    if request.method == 'POST':
        category_title = request.POST.get('category_title')

        Category.objects.create(title=category_title)

        return redirect('categorylist')  

    return render(request, 'adminauth/add_category.html')

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('categorylist')  # Replace 'category_list' with the URL name of your category list view
    return render(request, 'adminauth/category_delete_confirm.html', {'category': category})

def add_product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        marked_price = int(request.POST.get('marked_price'))
        selling_price = int(request.POST.get('selling_price'))
        description = request.POST.get('description')
        view_count = int(request.POST.get('view_count'))
        is_available = bool(request.POST.get('is_available'))
        image = request.FILES.get('image')  # If you have an image field, retrieve it from request.FILES

        # Create the new product object
        product = Product.objects.create(
            title=title,
            category_id=category_id,
            marked_price=marked_price,
            selling_price=selling_price,
            description=description,
            view_count=view_count,
            is_available=is_available,
            image=image  # If you have an image field, include it in the create method
        )
        return redirect('productlist')  # Redirect to the product list view after adding a product
    

    return render(request, 'adminauth/add_product.html')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.title = request.POST.get('title')
        product.marked_price = request.POST.get('marked_price')
        product.selling_price = request.POST.get('selling_price')
        product.is_available = request.POST.get('is_available') == 'True'

        # Update the category if needed
        category_id = request.POST.get('category')
        if category_id:
            product.category_id = category_id

        product.save()

        # After successfully editing, you might want to redirect to the product list page
        return redirect('productlist')  # Replace 'productlist' with the name of the URL pattern for your product list page

    # If it's a GET request, render the edit product form
    return render(request, 'adminauth/edit_product.html', {'product': product})


def delete_product(request, product_id):
    # Get the product instance by its ID
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # If the request is a POST request, delete the product and redirect to the product list view.
        product.delete()
        return redirect('productlist')

    return render(request, 'adminauth/delete_product.html', {'product': product})

from django.shortcuts import render, redirect
from app.models import Variation

def add_variation(request):
    if request.method == 'POST':
        variation_category = request.POST.get('variation_category')
        variation_value = request.POST.get('variation_value')

        # Assuming you have a product_id associated with the variation,
        # you can retrieve the product instance based on the product_id.
        # Replace 'product_id' with the actual field name where the product ID is stored in your form.
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)

        # If the variation category is 'Size', add 'GB' to the variation value
        if variation_category == 'Size':
            variation_value = f'{variation_value} GB'
        elif variation_category == 'RAM':
            variation_value = f'{variation_value} GB RAM'  # Assuming RAM value is provided in GB

        # Create the new variation object
        variation = Variation.objects.create(
            product=product,
            variation_category=variation_category,
            variation_value=variation_value,
            # Add other fields as needed
        )
        return redirect('add_variant')  # Redirect to the add variation page after adding a variation

    return render(request, 'adminauth/add_variation.html')

def variantlist(request):

    variations = Variation.objects.all()

    return render(request, 'adminauth/variantlist.html', {'variations': variations})

def add_variation(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        variation_category = request.POST['variation_category']
        variation_value = request.POST['variation_value']
        is_active = request.POST['is_active']

        # Get the corresponding product using the product_id
        product = Product.objects.get(id=product_id)

        # Create a new Variation object and save it to the database
        variation = Variation(
            product=product,
            variation_category=variation_category,
            variation_value=variation_value,
            is_active=is_active == 'True'  # Convert 'True'/'False' string to boolean
        )
        variation.save()

        # Redirect back to the variation list or any other page
        return redirect('variantlist')

    # If the request method is GET, render the template with the products data
    products = Product.objects.all()
    return render(request, 'adminauth/add_variation.html', {'products': products})

def delete_variation(request, variation_id):
    variation = get_object_or_404(Variation, id=variation_id)

    if request.method == 'POST':
        variation.delete()
        return redirect('variantlist')

    context = {
        'variation': variation,
    }

    return render(request, 'adminauth/delete_variation.html', context)