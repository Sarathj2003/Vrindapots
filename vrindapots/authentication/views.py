import random
import re
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError



# Create your views here.



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('user_login')

    return render(request,'login.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    logout(request)
    return redirect('user_login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # 1. Check if email is empty
        if not email:
            messages.error(request, "Email cannot be blank.")
            return redirect('user_signup')

        # 2. Validate email format using regex
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messages.error(request, "Invalid email format.")
            return redirect('user_signup')

        # 3. Check if passwords are empty
        if not password1 or not password2:
            messages.error(request, "Password fields cannot be blank.")
            return redirect('user_signup')

        # 4. Validate password length and complexity
        if len(password1) < 8 or not re.search(r'\d', password1):
            messages.error(request, "Password must be at least 8 characters long and include a number.")
            return redirect('user_signup')

        # 5. Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('user_signup')

        # 6. Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('user_signup')

        # 7. Generate OTP and store user details in session temporarily
        otp = random.randint(100000, 999999)
        request.session['otp'] = str(otp)
        request.session['email'] = email
        request.session['password'] = password1

        send_mail(
            'Your OTP for registration in vrindapots',
            f'Your OTP for registration in vrindapots : {otp}',
            'sarathjayakumar46@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect('verify_otp')

    return render(request, 'signup.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        user.profile.address = address
        user.phone_number = phone_number
        user.profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('home')
    return render(request, 'profile_update.html')



def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        sent_otp = request.session.get('otp')
        email = request.session.get('email')
        password = request.session.get('password')

        if str(entered_otp) == str(sent_otp):
            user = User.objects.create_user(username=email, email=email, password=password)
            user.is_active = True
            user.save()

            del request.session['otp']
            del request.session['email']
            del request.session['password']

            messages.success(request, 'Your account has been activated successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')
        
    return render(request, 'verify_otp.html',)


# def validate_email(email):
#     try:
#         django_validate_email(email)
#         return True
#     except ValidationError:
#         return False

# def validate_password(password):
#     return re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password) is not None