from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from authentication.models import Profile
from store.models import Category,Product
from .forms import CategoryForm, ProductForm

# Create your views here.


def admin_home(request):
    return render(request,'admin_templates/admin_home.html')

def user_list(request):
    users = User.objects.all()
    return render(request, 'admin_templates/user_list.html', {'users': users})

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user) 

    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f'User  {user.username} has been {"unblocked" if user.is_active else "blocked"}.')
        return redirect('user_list')

    return render(request, 'admin_templates/user_detail.html', {'user': user, 'profile': profile})



def category_list(request):
    categories = Category.objects.all()  
    return render(request, 'admin_templates/category_list.html', {'categories': categories})

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

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.soft_delete()
    messages.success(request, 'Category soft deleted successfully!')
    return redirect('category_list') 

def category_restore(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.restore()
    messages.success(request, 'Category restored successfully!')
    return redirect('category_list')

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



def product_list(request):
    products = Product.objects.all()  
    return render(request, 'admin_templates/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')  # Redirect to the list of products or wherever you want
        else:
            messages.error(request, 'There was an error adding the product. Please correct the errors below.')
    else:
        form = ProductForm()

    return render(request, 'admin_templates/add_product.html', {
        'form': form,
    })


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Retrieve the product instance
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # Bind the form to the product instance
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')  # Redirect to the list of products
        else:
            messages.error(request, 'There was an error updating the product. Please correct the errors below.')
    else:
        form = ProductForm(instance=product)  # Pre-fill the form with the product's data

    return render(request, 'admin_templates/edit_product.html', {
        'form': form,
        'product': product,  # Pass the product for reference (e.g., to show the name)
    })


def soft_delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.soft_delete()  
    return redirect('product_list')

def restore_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.restore()  
    return redirect('product_list')

def delete_product(request, product_id):
    # Fetch the product using the primary key
    product = get_object_or_404(Product, id=product_id)
    
    # Delete the product permanently
    product.images.all().delete()  # Optionally delete related images
    product.delete()  # This will call the default delete method

    return redirect('product_list')