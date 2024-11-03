from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from authentication.models import Profile
from store.models import Category,Product
from .forms import CategoryForm, ProductForm

# Create your views here.



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def custom_admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:  
                login(request, user)
                return redirect('admin_home')  
            else:
                messages.error(request, 'You do not have permission to access the admin panel.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'admin_templates/custom_admin_login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def custom_admin_logout(request):
    logout(request)
    return redirect('custom_admin_login')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def admin_home(request):
    return render(request,'admin_templates/admin_home.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin_templates/user_list.html', {'users': users})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user) 
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f'User  {user.username} has been {"unblocked" if user.is_active else "blocked"}.')
        return redirect('user_list')
    return render(request, 'admin_templates/user_detail.html', {'user': user, 'profile': profile})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def category_list(request):
    categories = Category.objects.all()  
    return render(request, 'admin_templates/category_list.html', {'categories': categories})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')  
    else:
        form = CategoryForm()
    return render(request, 'admin_templates/category_form.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.soft_delete()
    messages.success(request, 'Category soft deleted successfully!')
    return redirect('category_list') 



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def category_restore(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.restore()
    messages.success(request, 'Category restored successfully!')
    return redirect('category_list')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)  
    if request.method == 'POST':
        if 'delete' in request.POST:  
            category.delete()  
            messages.success(request, 'Category deleted successfully!')
            return redirect('category_list') 
        else:
            form = CategoryForm(request.POST, instance=category)  
            if form.is_valid():
                form.save()  
                messages.success(request, 'Category edited successfully!')
                return redirect('category_list')  
    else:
        form = CategoryForm(instance=category)  
    return render(request, 'admin_templates/edit_category.html', {'form': form, 'category': category})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def product_list(request):
    products = Product.objects.all()  
    return render(request, 'admin_templates/product_list.html', {'products': products})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')  
        else:
            messages.error(request, 'There was an error updating the product. Please correct the errors below.')
    else:
        form = ProductForm()
    return render(request, 'admin_templates/add_product.html', {
        'form': form,
    })



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)  
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')  
        else:
            messages.error(request, 'There was an error updating the product. Please correct the errors below.')
    else:
        form = ProductForm(instance=product)  
    return render(request, 'admin_templates/edit_product.html', {
        'form': form,
        'product': product, 
    })



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def soft_delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.soft_delete()  
    return redirect('product_list')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def restore_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.restore()  
    return redirect('product_list')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def delete_product(request, product_id): 
    product = get_object_or_404(Product, id=product_id)
    product.images.all().delete()  
    product.delete()  
    return redirect('product_list')