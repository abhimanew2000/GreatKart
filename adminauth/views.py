from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from userauths.models import User

# Create your views here.

def admin_panel(request):
    return render(request, 'adminauth/admin_panel.html')

def admin_signin(request):
    if request.method == "POST":
        # Your existing authentication logic

        # Change this line to redirect to the correct URL
        return redirect('admin_panel')  # Assuming 'admin_panel' is the correct URL name for your admin dashboard
    else:
        return render(request, 'adminsignin.html')  # Render the template without using 'redirect'



