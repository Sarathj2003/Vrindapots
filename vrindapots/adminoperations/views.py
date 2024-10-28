from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from authentication.models import Profile
from store.models import Category,Product, ProductImage
from .forms import CategoryForm, ProductForm, ProductImageForm, ImageCountForm

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
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added successfully!')

            # Redirect to the add images page for the newly created product
            return redirect('add_product_images', product_id=product.id)
        else:
            messages.error(request, 'There was an error adding the product. Please correct the errors below.')
    else:
        form = ProductForm()

    return render(request, 'admin_templates/add_product.html', {
        'form': form,
    })

def add_product_images(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        
        if 'image_count' in request.POST:
            image_count = int(request.POST['image_count'])
            image_indices = list(range(image_count))
            return render(request, 'admin_templates/upload_images.html', {
                'product': product,
                'image_count': image_count,
                'image_indices': image_indices,
            })
        
        else:

            image_files = [request.FILES.get(f'image_{i}') for i in range(int(request.POST['image_count'])) if request.FILES.get(f'image_{i}')]

            if not image_files:
                messages.error(request, 'Please upload at least one image.')
                return redirect('add_product_images', product_id=product.id)

            # Save each image to the database
            for image_file in image_files:
                try:
                    if image_file:
                        ProductImage.objects.create(product=product, image=image_file)
                except Exception as e:
                    print("Error saving image:", e)
                    messages.error(request, f"Failed to save an image: {e}")
                    return redirect('add_product_images', product_id=product.id)

            messages.success(request, 'Images uploaded successfully!')
            return redirect('product_list')

    form = ImageCountForm()
    return render(request, 'admin_templates/select_image_count.html', {
        'form': form,
        'product': product,
    })


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        if 'delete' in request.POST:  
            product.delete()  
            messages.success(request, 'Product deleted successfully!')
            return redirect('product_list') 
        else:
            product_form = ProductForm(request.POST, instance=product)
            if product_form.is_valid():
                product_form.save()
                
                for i in range(4):  
                    image_form = ProductImageForm(request.POST, request.FILES, prefix=f'image_{i}')
                    if image_form.is_valid():
                        product_image = image_form.save(commit=False)
                        product_image.product = product
                        if i == 0:  
                            product_image.is_main = True
                        else:
                            product_image.is_main = False
                        product_image.save()
                return redirect('product_list')  
    else:
        product_form = ProductForm(instance=product)  

    return render(request, 'admin_templates/edit_product.html', {
        'product_form': product_form,
        'product': product,
        'image_count': range(4)  
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