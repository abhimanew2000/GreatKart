from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path("signup/", views.handlesignup, name='handlesignup'),
    path("signin/", views.handlelogin, name='handlelogin'),
    path("signout/", views.handlelogout, name='handlelogout'),
]
