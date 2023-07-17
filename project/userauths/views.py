from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from userauths.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

user = settings.AUTH_USER_MODEL
def handlesignup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hey {username}, your account was successfully created.")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('app:index')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'userauths/signup.html', context)


def handlelogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, f"User with {email} does not exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"You are logged in")
            return redirect('app:index')
        else:
            messages.warning(request, f"User does not exist")

    return render(request, "userauths/signin.html")

def handlelogout(request):
    logout(request)
    
    return redirect('app:index')


