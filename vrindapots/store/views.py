from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Category,Product,Tag,Banner,Review,Wishlist,Cart,CartItem,OrderItem,Order
from authentication.models import Profile,User
from django.db.models import F, ExpressionWrapper, FloatField, Avg, Count, Q, Value
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Coalesce
from django.db.models import Prefetch
from django.contrib import messages
from django.http import Http404
from decimal import Decimal
from django.db import transaction
# Create your views here.





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def home_page(request):
    sort_by = request.GET.get('sort_by')
    sort_options = {
        'popularity': '-popularity',          
        'price_low_high': 'new_price',            
        'price_high_low': '-new_price',           
        'ratings': '-average_rating',         
        'a_to_z': 'name',                     
        'z_to_a': '-name',                    
    }
    sort_order = sort_options.get(sort_by, 'average_rating')
    banner = Banner.objects.first()

    Exclusive_Offer_products = Product.objects.filter(
        tag__name='Exclusive Offers',
        category__is_deleted=False,
        is_deleted = False
    ).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'), 
        average_rating=Coalesce(Avg('reviews__rating'), Value(0, output_field=FloatField())),  
        rating_percentage=Coalesce(Avg('reviews__rating') * 20, Value(0, output_field=FloatField()))
    ).order_by(sort_order)[:3] 

    Best_Seller_products = Product.objects.filter(
        tag__name='Best Sellers',
        category__is_deleted=False,
        is_deleted = False
    ).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'), 
        average_rating=Coalesce(Avg('reviews__rating'), Value(0, output_field=FloatField())),  
        rating_percentage=Coalesce(Avg('reviews__rating') * 20, Value(0, output_field=FloatField()))
    ).order_by(sort_order)[:3]  

    New_Arrivals_products = Product.objects.filter(
        tag__name='New Arrivals',
        category__is_deleted=False,
        is_deleted = False
    ).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'), 
        average_rating=Coalesce(Avg('reviews__rating'), Value(0, output_field=FloatField())),  
        rating_percentage=Coalesce(Avg('reviews__rating') * 20, Value(0, output_field=FloatField()))
    ).order_by(sort_order)[:3] 

    Seasonal_Specials_products = Product.objects.filter(
        tag__name='Seasonal Specials',
        category__is_deleted=False,
        is_deleted = False
    ).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'), 
        average_rating=Coalesce(Avg('reviews__rating'), Value(0, output_field=FloatField())),  
        rating_percentage=Coalesce(Avg('reviews__rating') * 20, Value(0, output_field=FloatField()))
    ).order_by(sort_order)[:3]  

    return render(request, 'home.html', {
        'banner': banner,
        'Exclusive_Offer_products': Exclusive_Offer_products,
        'Best_Seller_products': Best_Seller_products,
        'New_Arrivals_products': New_Arrivals_products,
        'Seasonal_Specials_products': Seasonal_Specials_products,
        'show_button': True,
    })



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def all_products_page(request):
    sort_by = request.GET.get('sort_by')
    sort_options = {
        'popularity': '-popularity',          
        'price_low_high': 'new_price',            
        'price_high_low': '-new_price',           
        'ratings': '-average_rating',         
        'a_to_z': 'name',                     
        'z_to_a': '-name',                    
    }
    sort_order = sort_options.get(sort_by, 'average_rating')

    banner = Banner.objects.first()
    all_products = Product.objects.filter(category__is_deleted=False,is_deleted = False).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'), 
        average_rating=Coalesce(Avg('reviews__rating'), Value(0, output_field=FloatField())),  
        rating_percentage=Coalesce(Avg('reviews__rating') * 20, Value(0, output_field=FloatField()))  
    ).order_by(sort_order)

    return render(request, 'all_products.html', {
        'banner': banner,
        'all_products': all_products,
        'show_button': True,
    })



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def category_products_page(request, id):
    sort_by = request.GET.get('sort_by')
    sort_options = {
        'popularity': '-popularity',          
        'price_low_high': 'new_price',            
        'price_high_low': '-new_price',           
        'ratings': '-average_rating',         
        'a_to_z': 'name',                     
        'z_to_a': '-name',                    
    }
    sort_order = sort_options.get(sort_by, 'average_rating')

    banner = Banner.objects.first()
    category_name = Category.objects.filter(id=id).first()
    category_products = Product.objects.filter(category__id=id,category__is_deleted=False ,is_deleted=False).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'),  
        average_rating=Coalesce(Avg('reviews__rating'), Value(0, output_field=FloatField())),  
        rating_percentage=Coalesce(Avg('reviews__rating') * 20, Value(0, output_field=FloatField()))  
    ).order_by(sort_order)
    return render(request, 'category_products.html', {
        'banner': banner,
        'category_products': category_products,
        'category_name': category_name,
        'show_button': True,
    })



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def tag_products_page(request, id):
    sort_by = request.GET.get('sort_by')
    sort_options = {
        'popularity': '-popularity',          
        'price_low_high': 'new_price',            
        'price_high_low': '-new_price',           
        'ratings': '-average_rating',         
        'a_to_z': 'name',                     
        'z_to_a': '-name',                    
    }
    sort_order = sort_options.get(sort_by, 'average_rating')
    banner = Banner.objects.first()
    tag_name = Tag.objects.filter(id=id).first()
    tag_products = Product.objects.filter(tag__id=id,category__is_deleted=False ,is_deleted=False).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'),  
        average_rating=Coalesce(Avg('reviews__rating'), Value(0, output_field=FloatField())),  
        rating_percentage=Coalesce(Avg('reviews__rating') * 20, Value(0, output_field=FloatField()))  
    ).order_by(sort_order)
    return render(request, 'tag_products.html', {
        'banner': banner,
        'tag_products': tag_products,
        'tag_name': tag_name,
        'show_button': True,
    })



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    average_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = Review.objects.filter(product=product).count()
    reviews = Review.objects.filter(product=product).select_related('user').order_by('-created_at')
    rating_percentage = average_rating * 20
    related_products = Product.objects.filter(
    Q(category=product.category) & 
    ~Q(id=product.id) & 
    Q(category__is_deleted=False) &     
    Q(is_deleted=False)
    ).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'),  
        average_rating=Coalesce(Avg('reviews__rating'), Value(0, output_field=FloatField())),  
        rating_percentage=Coalesce(Avg('reviews__rating') * 20, Value(0, output_field=FloatField()))  
    )[:3] 
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating is not None and comment is not None:
            rating = int(rating)  
            if 0 <= rating <= 5:  
                review = Review(product=product, user=request.user, rating=rating, comment=comment)
                review.save()
                return redirect('product_detail', id=product.id)  
    context = {
        'product': product,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'reviews': reviews,
        'rating_percentage': rating_percentage,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, 'Product added to wishlist.')
    else:
        messages.error(request, 'Product is already in your wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist')  


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).order_by('id')
    total_cost = Decimal(0)  
    # cart_updated = False  
    print(cart_items)
    for item in cart_items:
        # if item.quantity > item.product.stock:
        #     if item.product.stock == 0:
        #         messages.warning(request, f"'{item.product.name}' is out of stock! Please remove the item from your cart to proceed.")
        #     else:
        #         messages.warning(request, f"Only {item.product.stock} units of '{item.product.name}' available! Please update your cart to proceed.")
            
            
            # item.quantity = item.product.stock
            # item.save()
            # cart_updated = True  
            # messages.warning(request, f"The quantity of '{item.product.name}' has been adjusted to {item.product.stock} due to limited stock.")
                
        item.subtotal = item.product.new_price * item.quantity  
        total_cost += item.subtotal  
    request.session['total'] = float(total_cost)

    return render(request, 'cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_cost': total_cost  
    })



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    if product.stock == 0:
        messages.error(request, "No stock available")
        return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))
    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} units available in stock.")
        return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))
    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
        return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))
   
    if product.stock < quantity:
        messages.error(request, "Not enough stock available.")
        return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = quantity
    else:
        if product.stock < cart_item.quantity + quantity:
            messages.error(request, "Not enough stock available.")
            return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))
        cart_item.quantity += quantity  
    cart_item.save()
    messages.success(request, f"Added {quantity} of {product.name} to your cart.")
    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    messages.success(request, "Removed item from your cart.")
    return redirect('cart_detail')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def update_cart_item_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product = cart_item.product 
    new_quantity = int(request.POST.get("quantity", cart_item.quantity))
    # if new_quantity > product.stock:
    #     messages.error(request, f"Only {product.stock} units available in stock.")

    if new_quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
    else:            
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f"Quantity updated to {new_quantity}.")
    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def checkout(request):
    profile = get_object_or_404(Profile, user=request.user, is_current=True)
    profiles = Profile.objects.filter(user=request.user).order_by('id')
    full_name = f"{request.user.first_name} {request.user.last_name}".strip()
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart, quantity__gt=0).order_by('id')
    
    for item in cart_items:
        if item.quantity > item.product.stock:
            if item.product.stock == 0:
                messages.warning(request, f"'{item.product.name}' is out of stock! Please remove the item from your cart to proceed.")
            else:
                messages.warning(request, f"Only {item.product.stock} units of '{item.product.name}' available! Please update your cart to proceed.")
            return redirect('cart_detail')

    total_cost = 0
    for item in cart_items:
        item.subtotal = item.product.new_price * item.quantity
        total_cost += item.subtotal
    request.session['previous_page'] = request.get_full_path()
    
    return render(request, 'checkout_page.html', {
        'full_name': full_name,
        'profile': profile,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'profiles': profiles,
    })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
@transaction.atomic
def place_order(request):
    if request.method == "POST":
        profile = get_object_or_404(Profile, user=request.user, is_current=True)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, quantity__gt=0)
        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect("cart")
        total_cost = sum(item.product.new_price * item.quantity for item in cart_items)
        shipping_address = profile.address
        shipping_pincode = profile.pincode
        shipping_phone_number = profile.phone_number
        shipping_state = profile.state
        order = Order.objects.create(
            user=request.user,
            status="Pending",
            total_price=total_cost,
            payment_method="COD", 
            shipping_address=shipping_address,
            shipping_pincode=shipping_pincode,
            shipping_phone_number=shipping_phone_number,
            shipping_state=shipping_state,
            is_paid=False  
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.new_price
            )
            item.product.stock -= item.quantity
            item.product.save()
        cart_items.delete()
        delivery_date = order.delivery_date
        messages.success(request, "Order placed successfully!")
        return redirect('home')
    else:
        return redirect("checkout_page")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'my_orders.html', {'orders': orders})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        item.subtotal = item.quantity * item.price
    total_cost = order.total_price
    return render(request, 'order_detail.html', {
        'order': order,
        'order_items': order_items,
        'total_cost': total_cost
    })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'Cancelled':
        order.status = 'Cancelled'
        order.save()
        for item in order.order_items.all():  
            item.product.stock += item.quantity
            item.product.save()
        messages.success(request, "Order cancelled!")
    return redirect('my_orders')
