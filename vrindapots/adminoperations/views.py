from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from authentication.models import Profile
from store.models import Category,Product, Order,OrderItem,Coupon
from .forms import CategoryForm, ProductForm, CouponForm
from django.db import transaction
from django.http import HttpResponse
from django.db.models import Sum, F
from datetime import datetime, timedelta
from weasyprint import HTML
from django.http import JsonResponse
from django.db.models.functions import TruncDay,TruncYear,TruncMonth
from django.utils.timezone import now

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
    top_products = (
        OrderItem.objects.values('product__name')
        .annotate(total_sales=Sum('quantity'))
        .order_by('-total_sales')[:10]
    )

    
    top_categories = (
        OrderItem.objects.values('product__category__name')
        .annotate(total_sales=Sum('quantity'))
        .order_by('-total_sales')[:3]
    )
    
    context = {
        'top_products': top_products,
        'top_categories': top_categories,
    }
    
    return render(request,'admin_templates/admin_home.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def sales_chart(request):
    daily_data = (
        Order.objects.filter(status='Delivered')
        .annotate(day=TruncDay('order_date')) 
        .values('day')  
        .annotate(total_sales=Sum('total_price'))  
        .order_by('day')  
    )

    
    monthly_data = (
        Order.objects.filter(status='Delivered')  
        .annotate(month=TruncMonth('order_date'))  
        .values('month')  
        .annotate(total_sales=Sum('total_price'))  
        .order_by('month')  
    )

   
    yearly_data = (
        Order.objects.filter(status='Delivered')  
        .annotate(year=TruncYear('order_date'))  
        .values('year')  
        .annotate(total_sales=Sum('total_price'))  
        .order_by('year') 
    )

    
    daily_labels = [entry['day'].strftime('%Y-%m-%d') for entry in daily_data]
    daily_sales = [entry['total_sales'] for entry in daily_data]

    
    monthly_labels = [entry['month'].strftime('%B') for entry in monthly_data]
    monthly_sales = [entry['total_sales'] for entry in monthly_data]

    yearly_labels = [entry['year'].strftime('%Y') for entry in yearly_data]
    yearly_sales = [entry['total_sales'] for entry in yearly_data]


    return JsonResponse({
        'daily':{
            'labels':daily_labels,
            'data':daily_sales,
        },
        'monthly':{
            'labels':monthly_labels,
            'data':monthly_sales,
        },
        'yearly':{
            'labels':yearly_labels,
            'data':yearly_sales
        }
    })




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def user_list(request):
    users = User.objects.exclude(is_staff=True).order_by('id')
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
    products = Product.objects.all().order_by('id')  
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
            if new_status == "Delivered":
                order.delivery_date = now()
            order.save()
            messages.success(request, "Order status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")
        return redirect("admin_order_details", order_id=order.id)

    if order.status == 'Pending':
        status_choices = [
            (choice[0], choice[1]) for choice in Order.STATUS_CHOICES if choice[0] != order.status and (choice[0] == 'Delayed' or choice[0] == 'Delivered')
        ]
    elif order.status == 'Delayed':
        status_choices = [
            (choice[0], choice[1]) for choice in Order.STATUS_CHOICES if choice[0] != order.status and (choice[0] == 'Pending' or choice[0] == 'Delivered')
        ]
    else:
        status_choices = [
            (choice[0], choice[1]) for choice in Order.STATUS_CHOICES if choice[0] != order.status and choice[0] != 'Cancelled' and choice[0] != 'Returned'
        ]
    




    # status_choices = [
    #         (choice[0], choice[1]) for choice in Order.STATUS_CHOICES if choice[0] != order.status and choice[0] != 'Cancelled' and choice[0] != 'Returned'
    #     ]

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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def change_to_returned(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'Return':
        order.status = 'Returned'
        order.return_date = now()
        order.save()
        messages.success(request, f"Order #{order.id} has been returned.")
    return redirect('admin_order_details', order_id=order.id)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def coupon_list_page(request):
    coupons = Coupon.objects.all().order_by('id')

    return render(request,'admin_templates/coupon_list.html',{
        'coupons': coupons,
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def add_coupon(request):
    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon added successfully!")
            return redirect('coupon_list_page') 
        else:
            messages.error(request, "There was an error adding the coupon. Please check the form.")
    else:
        form = CouponForm()
    
    
    return render(request, 'admin_templates/add_coupon.html', {
        'form': form
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)

    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Coupon updated successfully!')
            return redirect('coupon_list_page')  
        else:
            messages.error(request, 'Error updating coupon. Please check the form and try again.')
    else:
        form = CouponForm(instance=coupon)  

    return render(request, 'admin_templates/edit_coupon.html', {'form': form, 'coupon': coupon})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    coupon.delete()
    messages.success(request, "Coupon deleted successfully.")
    return redirect('coupon_list_page') 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='custom_admin_login')
def sales_report(request):
    # Get filter type from request
    filter_type = request.GET.get('filter', 'None')
    
    # Get custom start and end dates if provided
    custom_start_date = request.GET.get('custom_start_date')
    custom_end_date = request.GET.get('custom_end_date')

    today = datetime.now()

    # Initialize start_date and end_date
    start_date = today
    end_date = today  # Default end_date is today if no custom range is provided

    # Set the start date based on the filter type or custom date range
    if filter_type == 'day':
        start_date = today
    elif filter_type == 'week':
        start_date = today - timedelta(days=7)
    elif filter_type == 'month':
        start_date = today - timedelta(days=30)
    elif custom_start_date and custom_end_date:
        start_date = datetime.strptime(custom_start_date, '%Y-%m-%d')
        end_date = datetime.strptime(custom_end_date, '%Y-%m-%d')

    # Filter orders based on the selected date range
    if custom_start_date and custom_end_date:
        orders = Order.objects.filter(order_date__range=(start_date, end_date), status='Delivered').order_by('order_date')
    else:
        orders = Order.objects.filter(order_date__gte=start_date, status='Delivered').order_by('order_date')

    total_sales = orders.aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
    total_orders = orders.count()
    total_items = OrderItem.objects.filter(order__in=orders).aggregate(
        total_items=Sum('quantity')
    )['total_items'] or 0

    if 'download_pdf' in request.GET:
        html_template = 'admin_templates/sales_report_pdf.html'
        context = {
            'orders': orders,
            'total_sales': total_sales,
            'total_orders': total_orders,
            'total_items': total_items,
            'filter_type': filter_type,
            'custom_start_date': custom_start_date,
            'custom_end_date': custom_end_date,
        }
        html_string = render(request, html_template, context).content.decode('utf-8')
        pdf = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="sales_report_{filter_type}.pdf"'
        return response

    context = {
        'orders': orders,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_items': total_items,
        'filter_type': filter_type,
        'custom_start_date': custom_start_date,
        'custom_end_date': custom_end_date,
    }
    return render(request, 'admin_templates/sales_report.html', context)





