from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from authentication.models import Profile
from store.models import Category,Product, Order,OrderItem
from .forms import CategoryForm, ProductForm
from django.db import transaction

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
    profiles = Profile.objects.filter(user=user)  

    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f'User {user.username} has been {"unblocked" if user.is_active else "blocked"}.')
        return redirect('user_list')

    return render(request, 'admin_templates/user_detail.html', {'user': user, 'profiles': profiles})


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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def admin_order_list(request):
    orders = Order.objects.all().order_by('-order_date')  
    return render(request, 'admin_templates/order_list.html', {'orders': orders})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def admin_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = []

    for item in order.order_items.all():
        item.subtotal = item.product.new_price * item.quantity
        order_items.append(item)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status and new_status != order.status:
            order.status = new_status
            order.save()
            messages.success(request, "Order status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")
        return redirect("admin_order_details", order_id=order.id)

    # Exclude the current status from the dropdown
    status_choices = [
        (choice[0], choice[1]) for choice in Order.STATUS_CHOICES if choice[0] != order.status and choice[0] != 'Cancelled'
    ]

    return render(request, 'admin_templates/admin_order_details.html', {
        'order': order,
        'order_items': order_items,
        'status_choices': status_choices,
    })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def admin_order_cancel(request, order_id):
    with transaction.atomic():
        order = get_object_or_404(Order, id=order_id)
        if order.status == 'Pending':
            for item in order.order_items.all():
                product = item.product
                product.stock += item.quantity
                product.save()
            order.status = 'Cancelled'
            order.save()
            messages.success(request, f"Order #{order.id} has been cancelled and stock updated.")
        else:
            messages.error(request, f"Order #{order.id} cannot be cancelled.")

    return redirect('admin_order_details', order_id=order.id)



    
