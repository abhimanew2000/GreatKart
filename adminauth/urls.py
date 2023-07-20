# adminauth/urls.py
from django.urls import path
from adminauth import views

urlpatterns = [
    path('admin_signin', views.admin_signin, name='admin_signin'), 
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('userinfo', views.userinfo, name='userinfo'),
]
