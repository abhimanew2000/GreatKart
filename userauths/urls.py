from django.urls import path
from userauths import views



urlpatterns = [
    path("handlesignup", views.handlesignup, name='handlesignup'),
    path("handlelogin", views.handlelogin, name='handlelogin'),
    path("handlelogout", views.handlelogout, name='handlelogout'),
    path("otp_verify", views.otp_verify, name='otp_verify'),  # Add this line for OTP verification

    

]
