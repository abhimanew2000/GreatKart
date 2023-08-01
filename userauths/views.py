from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User
from carts.models import Carts,CartItem


import random
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# ----------------------------------Reset password imports-----------------------------------------------------------------------
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model, views as auth_views
# ----------------------------------------------------------------------------------------------

from carts.views import _cart_id

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
    else:
    
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

            try:
                cart=Carts.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user=user
                        item.save()
            except:
                pass
            login(request, user)
            messages.success(request, f"You are logged in")
            return redirect('index')
        else:
            messages.warning(request, f"User does not exist")

    return render(request, "userauths/handlelogin.html")

def handlelogout(request):
    logout(request)
    
    return redirect('index')
@login_required(login_url='handlelogin')
def dashboard(request):
    return render(request,'userauths/dashboard.html')

# --------------------------Reset password view--------------------------------------------------
User = get_user_model()

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate password reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Build the reset link URL
            reset_url = f"{request.scheme}://{request.get_host()}/userauths/reset-password-confirm/{uid}/{token}/"

            # Send the password reset email
            subject = 'Password Reset'
            message = render_to_string('userauths/reset_password_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, 'Password reset link sent to your email.')
            return redirect('handlelogin')
        else:
            messages.error(request, 'User with this email does not exist.')
            return redirect('reset_password')

    return render(request, 'userauths/reset_password.html')


def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode URLsafe base64 and convert to string
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password reset successful. You can now log in with your new password.')
                return redirect('handlelogin')
        else:
            form = SetPasswordForm(user)

        return render(request, 'userauths/reset_password_confirm.html', {'form': form})
    else:
        messages.error(request, 'Invalid password reset link. Please try again.')
        return redirect('handlelogin')















