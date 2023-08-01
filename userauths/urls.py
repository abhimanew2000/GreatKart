from django.urls import path
from userauths import views



urlpatterns = [
    path("handlesignup", views.handlesignup, name='handlesignup'),
    path("handlelogin", views.handlelogin, name='handlelogin'),
    path("handlelogout", views.handlelogout, name='handlelogout'),
    path("dashboard", views.dashboard, name='dashboard'),
    path('reset-password', views.reset_password, name='reset_password'),
    path('reset-password-confirm/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),

   


    path("otp_verify", views.otp_verify, name='otp_verify'),  # Add this line for OTP verification

    

]
