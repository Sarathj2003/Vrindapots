import random
import re
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError
from .models import Profile



# Create your views here.



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email:
            messages.error(request, "Email cannot be blank.")
            return redirect('user_login')
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messages.error(request, "Invalid email format.")
            return redirect('user_login')
        if not password:
            messages.error(request, "Password cannot be blank.")
            return redirect('user_login')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('user_login')
    return render(request, 'login.html')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    messages.success(request, 'Your have logged out successfully!')
    return redirect('user_login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not email:
            messages.error(request, "Email cannot be blank.")
            return redirect('user_signup')
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messages.error(request, "Invalid email format.")
            return redirect('user_signup')
        if not password1 or not password2:
            messages.error(request, "Password fields cannot be blank.")
            return redirect('user_signup')
        if len(password1) < 8 or not re.search(r'\d', password1):
            messages.error(request, "Password must be at least 8 characters long and include a number.")
            return redirect('user_signup')
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('user_signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('user_signup')
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

def account_page(request):
    user = request.user
    profiles = Profile.objects.filter(user=user)
    # Handle user details update
    if request.method == 'POST' and 'update_user_details' in request.POST:
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.email = request.POST.get('email')
        
        user.save()
        return redirect('account_page')  # Refresh the page after save
    return render(request, 'account_page.html', {'user': user, 'profiles': profiles})

def edit_user_details(request, user_id):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        return redirect('account_page')  # Redirect back to the account page after saving

    return render(request, 'edit_user_details.html', {'user': user})



def set_current_address(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    Profile.objects.filter(user=request.user, is_current=True).update(is_current=False)
    profile.is_current = True
    profile.save()
    return redirect('account_page')

def add_new_address(request):
    if request.method == 'POST':
        # Collect address data from the form
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        phone_number = request.POST.get('phone_number')
        state = request.POST.get('state')
        
        if not re.match(r'^\d{10}$', phone_number):
            messages.error(request, 'Phone number must be exactly 10 digits and contain only numbers.')
            return render(request, 'add_address.html')
        
        if not re.match(r'^\d{6}$', pincode):
            messages.error(request, 'Pincode must be exactly 6 digits and contain only numbers.')
            return render(request, 'add_address.html')
        # Save new address
        Profile.objects.create(
            user=request.user,
            address=address,
            pincode=pincode,
            phone_number=phone_number,
            state=state
        )
        messages.success(request, 'New address added successfully!')
        return redirect('account_page')
    return render(request, 'add_address.html')



def edit_address(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    if request.method == 'POST':

        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')        
        if not re.match(r'^\d{10}$', phone_number):
            messages.error(request, 'Phone number must be exactly 10 digits and contain only numbers.')
            return render(request, 'edit_address.html',{'profile': profile})
        
        if not re.match(r'^\d{6}$', pincode):
            messages.error(request, 'Pincode must be exactly 6 digits and contain only numbers.')
            return render(request, 'edit_address.html',{'profile': profile})


        # Update the profile details from the form
        profile.address = address
        profile.pincode = pincode
        profile.phone_number = phone_number
        profile.state = state
        profile.save()
        return redirect('account_page')
    
    return render(request, 'edit_address.html', {'profile': profile})

def delete_address(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    if request.method == 'POST':
        profile.delete()
        return redirect('account_page')
    messages.error(request, 'Invalid operation')
    return redirect('account_page')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def profile_view(request):
    user = request.user
    profile = user.profile  
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        if not re.match(r'^\d{10}$', phone_number):
            messages.error(request, 'Phone number must be exactly 10 digits and contain only numbers.')
            return render(request, 'profile_update.html', {
                'user': user,
                'profile': profile,
            })
        if not re.match(r'^\d{6}$', pincode):
            messages.error(request, 'Pincode must be exactly 6 digits and contain only numbers.')
            return render(request, 'profile_update.html', {
                'user': user,
                'profile': profile,
            })
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        profile.address = address
        profile.phone_number = phone_number
        profile.pincode = pincode  
        profile.state = state      
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')
    return render(request, 'profile_update.html', {
        'user': user,
        'profile': profile,  
    })



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
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
            del request.session['otp']
            del request.session['email']
            del request.session['password']
            messages.success(request, 'Your account has been activated successfully!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')
    return render(request, 'verify_otp.html',)



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Email is not registered.")
            return redirect('forgot_password')
        otp = random.randint(100000, 999999)
        request.session['password_reset_otp'] = str(otp)
        request.session['reset_email'] = email
        send_mail(
            'Your OTP for Password Reset',
            f'Your OTP for Password Reset in vrindapots is: {otp}',
            'your-email@gmail.com',
            [email],
            fail_silently=False,
        )
        messages.success(request, "OTP sent to your email. Please check your inbox.")
        return redirect('verify_otp_for_password_reset')
    return render(request, 'forgot_password.html')



def verify_otp_for_password_reset(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        sent_otp = request.session.get('password_reset_otp')
        email = request.session.get('reset_email')
        if str(entered_otp) == str(sent_otp):
            messages.success(request, "OTP verified. Please reset your password.")
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp_for_password_reset')
    return render(request, 'verify_otp_for_password_reset.html')


def reset_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.session.get('reset_email')
        if not password1 or not password2:
            messages.error(request, "Password fields cannot be blank.")
            return redirect('reset_password')
        if len(password1) < 8 or not re.search(r'\d', password1):
            messages.error(request, "Password must be at least 8 characters long and include a number.")
            return redirect('reset_password')
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')
        user = User.objects.get(email=email)
        user.set_password(password1)
        user.save()
        messages.success(request, "Your password has been reset successfully. Please log in.")
        del request.session['password_reset_otp']
        del request.session['reset_email']
        return redirect('user_login')
    return render(request, 'reset_password.html')