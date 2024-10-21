import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth.decorators import login_required



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
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('user_signup')
        
        user = User.objects.create_user(username=email, email=email, password=password1)
        login(request, user)  # Automatically log the user in after registration
        return redirect('user_profile')

    return render(request,'signup.html')


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