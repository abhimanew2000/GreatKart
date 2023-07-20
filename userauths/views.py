from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User
import random
from django.core.mail import send_mail

user = settings.AUTH_USER_MODEL
# def handlesignup(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
    # #     if form.is_valid():
    # #         new_user = form.save()
    # #         username = form.cleaned_data.get('username')
    # #         messages.success(request, f"Hey {username}, your account was successfully created.")
    # #         new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
    # #         login(request, new_user)
    # #         return redirect('app:index')
    # # else:
    # #     form = UserRegisterForm()
    # # context = {
    # #     'form': form,
    # # }
    # return render(request, 'userauths/signup.html', context)

def handlesignup(request):
    # if 'email' in request.session:
    #     return redirect('index')    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            check_user = User.objects.filter(email=email).first()
            if check_user:
                messages.warning(request, "Email already exists")
                return redirect('handlesignup')
            
            request.session['registration_form_data'] = form.cleaned_data
            otp = random.randint(100000, 999999)
            request.session['otp'] = str(otp)
            send_mail(
                'OTP Verification',
                'Your OTP is ' + str(otp),
                'abhimanew2000@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('otp_verify')
    
    form = UserRegisterForm()
    return render(request, 'userauths/signup.html', {'form': form})




def otp_verify(request):
    if 'otp' in request.session: 
        if request.method == 'POST':
            otp = request.POST.get('otp')
            if otp == request.session.get('otp'):
                form_data = request.session.get('registration_form_data')
                form = UserRegisterForm(form_data)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.username = user.email.split("@")[0]
                    user.is_active = True
                    user.save()
                    messages.success(request, 'Registration Successful')
                    request.session.flush()
                    return redirect('handlelogin')
                else:
                    messages.error(request, 'Invalid form data')
                    return redirect('handlesignup')
            else:
                messages.error(request, 'Invalid OTP')
                return redirect('otp_verify')
        return render(request, 'userauths/otpverify.html')
    else:
        return redirect('handlesignup')



def handlelogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, f"User with {email} does not exist")

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_blocked==False:
            login(request, user)
            messages.success(request, f"You are logged in")
            return redirect('index')
        else:
            messages.warning(request, f"User does not exist")

    return render(request, "userauths/handlelogin.html")

def handlelogout(request):
    logout(request)
    
    return redirect('index')


