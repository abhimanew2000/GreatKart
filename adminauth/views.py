from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from userauths.models import User

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
            
    return render(request, 'adminauth/adminsignin.html')  # Render the template without using 'redirect'
    

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

def admin_panel(request):
    
    return render(request,'adminauth/admin_panel.html')



