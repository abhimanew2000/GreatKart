# adminauth/urls.py
from django.urls import path
from adminauth import views

urlpatterns = [
    path('admin_signin', views.admin_signin, name='admin_signin'), 
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('userinfo', views.userinfo, name='userinfo'),
    path('categorylist', views.categorylist, name='categorylist'),
    path('add_category', views.add_category, name='add_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('productlist', views.productlist, name='productlist'),
    path('add_product', views.add_product, name='add_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('add_variation/', views.add_variation, name='add_variation'),
    path('variantlist/', views.variantlist, name='variantlist'),
    path('delete_variation/<int:variation_id>/', views.delete_variation, name='delete_variation'),
    path('orderlist/', views.orderlist, name="orderlist"),








]
