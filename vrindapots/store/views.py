
import razorpay
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Category,Product,Tag,Banner,Review,Wishlist,Cart,CartItem,OrderItem,Order,Coupon,CouponUsage,Wallet
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
from django.utils import timezone

from datetime import timedelta
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
import io
import math
import json

# Create your views here.






@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def home_page(request):
    query = request.GET.get('q', '').strip()
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
def search_products(request):
    banner = Banner.objects.first()
    query = request.GET.get('q')
    all_products = []

    if query:
        all_products = Product.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query),
            is_deleted=False 
        )
    if not all_products:
        messages.warning(request, 'No products found matching your search criteria.')
        return redirect(request.META.get('HTTP_REFERER'))
        

    return render(request, 'search_page.html', {
        'all_products': all_products,
        'query':query,
        'banner':banner
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
        if not (request.user.first_name and request.user.last_name):
            messages.error(request, "Please complete your first name and last name in your profile to give rating and review.")
            return redirect('account_page')
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
    print(cart_items)
    for item in cart_items:
                
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
    try:
        profile = request.user.profile.first()
        if not (request.user.first_name and request.user.last_name):
            messages.error(request, "Please complete your first name and last name in your profile.")
            return redirect('account_page')
        if not profile or not (profile.address and profile.pincode and profile.phone_number and profile.state):
            messages.error(request, "Please complete all required profile details before proceeding to checkout.")
            return redirect('account_page')    
    except ObjectDoesNotExist:
        messages.error(request, "Please create your profile before proceeding to checkout.")
        return redirect('account_page')  

    try:
        del request.session['applied_coupon']
    except KeyError:
        pass
    try:
        wallet = request.user.wallet
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user)
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
            return redirect('checkout_page')

    total_cost = 0
    for item in cart_items:
        item.subtotal = item.product.new_price * item.quantity
        total_cost += item.subtotal

    subtotal_cost=total_cost

    coupon_code = request.POST.get('coupon_code', None)
    if coupon_code:
        try:
            current_date = now().date()
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            if current_date > coupon.end_date.date():
                messages.error(request, "This coupon is unavailable.")
                return redirect('checkout_page')

            usage_count = CouponUsage.objects.filter(coupon=coupon, user=request.user).count()
            if coupon.per_user_limit is not None and usage_count >= coupon.per_user_limit:
                messages.error(request, "You have already used this coupon.")
                return redirect('checkout_page')
            if coupon.discount_type == 'percentage':
                discount = (total_cost * coupon.discount_value) / 100
            else:
                discount = coupon.discount_value
            
            total_cost -= discount
            
            request.session['coupon_discount_type'] = coupon.discount_type
            request.session['discount_value'] = float(coupon.discount_value)
            request.session['applied_coupon'] = coupon_code 
            request.session['discount'] = float(discount)  
            request.session['total_cost'] = math.ceil(total_cost)  
            messages.success(request, f"Coupon '{coupon_code}' applied successfully!")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid or expired coupon code.")
        
    
    remove_coupon = request.POST.get('remove_coupon', None)
    if remove_coupon and 'applied_coupon' in request.session:
        discount = request.session.get('discount', 0)
        if isinstance(discount, float):  
            discount = Decimal(discount)
        total_cost += discount  
        del request.session['applied_coupon']  
        del request.session['discount']  
        del request.session['total_cost']
        messages.success(request, "Coupon removed successfully!")
        return redirect('checkout_page')

    delivery_fee=100


    current_time = timezone.now()
    available_coupons = Coupon.objects.filter(
        is_active=True, 
        start_date__lte=current_time, 
        end_date__gte=current_time
    )
    print(available_coupons)
    print(current_time)
    return render(request, 'checkout_page.html', {
        'full_name': full_name,
        'profile': profile,
        'cart_items': cart_items,
        'total_cost': math.ceil(total_cost)+delivery_fee,
        'subtotal_cost': subtotal_cost,
        'profiles': profiles,
        'applied_coupon': request.session.get('applied_coupon', None),
        'wallet_balance': wallet.balance,
        'delivery_fee': delivery_fee,
        'available_coupons':available_coupons,
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def place_order_cod(request):
    if request.method == "POST":
        payment_method = 'COD'
        profile = get_object_or_404(Profile, user=request.user, is_current=True)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, quantity__gt=0)
        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect('cart_detail')
        
        for item in cart_items:
            if item.quantity > item.product.stock:
                if item.product.stock == 0:
                    messages.warning(request, f"'{item.product.name}' is out of stock! Please remove the item from your cart to proceed.")
                else:
                    messages.warning(request, f"Only {item.product.stock} units of '{item.product.name}' available! Please update your cart to proceed.")
                return redirect('cart_detail')
            
        total_cost = Decimal(0)
        for item in cart_items:
            total_cost += item.product.new_price * item.quantity

        shipping_address = profile.address
        shipping_pincode = profile.pincode
        shipping_phone_number = profile.phone_number
        shipping_state = profile.state

        coupon = request.session.get('applied_coupon', None)
        discount = request.session.get('discount', None) 
        if coupon:
            coupon = get_object_or_404(Coupon, code=coupon)
            coupon_applied = True
        else:
            coupon_applied = False
        discount = Decimal(discount) if discount is not None else Decimal(0)
        
        final_cost = math.ceil(float(total_cost) - float(discount))

        # delivery charge = 100
        final_cost+=100 
        
        if final_cost > 1000:
            messages.warning(request, "Order above 1000 is not applicable for Cash on Delivery.")
            return redirect('checkout_page')

        order = Order.objects.create(
            user=request.user,
            status="Pending",
            total_price=final_cost,
            payment_method=payment_method,
            shipping_address=shipping_address,
            shipping_pincode=shipping_pincode,
            shipping_phone_number=shipping_phone_number,
            shipping_state=shipping_state,
            is_paid=False,  
            coupon_applied=coupon_applied,
            coupon=coupon,
            discount_amount=discount  
        )

        if coupon:
            CouponUsage.objects.create(
                coupon=coupon,
                user=request.user,
                order=order
            )

        try:
            del request.session['applied_coupon']
            del request.session['discount']
            del request.session['total_cost']
        except KeyError:
            pass

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
        order.save()
        return redirect('order_success', order_id=order.id)
    else:
        messages.warning(request, 'Something went wrong')
        return redirect(request.META.get('HTTP_REFERER', 'checkout_page'))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def place_order_wallet(request):
    payment_method = 'Wallet'
    profile = get_object_or_404(Profile, user=request.user, is_current=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart, quantity__gt=0)
    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')
    
    for item in cart_items:
        if item.quantity > item.product.stock:
            if item.product.stock == 0:
                messages.warning(request, f"'{item.product.name}' is out of stock! Please remove the item from your cart to proceed.")
            else:  
                messages.warning(request, f"Only {item.product.stock} units of '{item.product.name}' available! Please update your cart to proceed.")
            return redirect('cart_detail')
    
    total_cost = Decimal(0)   
    for item in cart_items:
        total_cost += item.product.new_price * item.quantity

    shipping_address = profile.address
    shipping_pincode = profile.pincode
    shipping_phone_number = profile.phone_number
    shipping_state = profile.state

    coupon = request.session.get('applied_coupon', None)
    discount = request.session.get('discount', None)
    if coupon:
        coupon = get_object_or_404(Coupon, code=coupon)
        coupon_applied = True
    else:
        coupon_applied = False
    discount = Decimal(discount) if discount is not None else Decimal(0)

    final_cost = math.ceil(float(total_cost) - float(discount))

    wallet = get_object_or_404(Wallet, user=request.user)
    if final_cost > wallet.balance:
        messages.error(request, "There is no enough money in the wallet to purchase.")
        return redirect('checkout_page')
    wallet.balance = wallet.balance - final_cost
    wallet.save()
    
    # delivery charge = 100
    final_cost+=100 

    order = Order.objects.create(
        user=request.user,
        status="Pending",
        total_price=final_cost,
        payment_method=payment_method,
        shipping_address=shipping_address,
        shipping_pincode=shipping_pincode,
        shipping_phone_number=shipping_phone_number,
        shipping_state=shipping_state,
        is_paid=True,  
        coupon_applied=coupon_applied,
        coupon=coupon,
        discount_amount=discount  
        )
    
    if coupon:
        CouponUsage.objects.create(
            coupon=coupon,
            user=request.user,
            order=order
        )

    try:
        del request.session['applied_coupon']
        del request.session['discount']
        del request.session['total_cost']
    except KeyError:
        pass

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
    order.save()
    return redirect('order_success', order_id=order.id)  

    


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def place_order_razorpay(request):
    if request.method == "POST":
        payment_method = 'Razorpay'
        profile = get_object_or_404(Profile, user=request.user, is_current=True)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, quantity__gt=0)
        
        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect('cart_detail')
        
        for item in cart_items:
            if item.quantity > item.product.stock:
                if item.product.stock == 0:
                    messages.warning(request, f"'{item.product.name}' is out of stock! Please remove the item from your cart to proceed.")
                else:
                    messages.warning(request, f"Only {item.product.stock} units of '{item.product.name}' available! Please update your cart to proceed.")
                return redirect('cart_detail')

        total_cost = Decimal(0)
        for item in cart_items:
            total_cost += item.product.new_price * item.quantity

        shipping_address = profile.address
        shipping_pincode = profile.pincode
        shipping_phone_number = profile.phone_number
        shipping_state = profile.state

        coupon = request.session.get('applied_coupon', None)
        discount = request.session.get('discount', None) 
        if coupon:
            coupon = get_object_or_404(Coupon, code=coupon)
            coupon_applied = True
        else:
            coupon_applied = False
        discount = Decimal(discount) if discount is not None else Decimal(0)

        if coupon_applied == True:
            final_cost = math.ceil(float(total_cost) - float(discount))
        else:
            final_cost = total_cost
    
        razorpay_order = razorpay_client.order.create({
            "amount": int(final_cost * 100), 
            "currency": "INR",
            "receipt": f"order_rcptid_{request.user.id}",
            "payment_capture": 1  
        })

        # delivery charge = 100
        final_cost+=100 
        
        order = Order.objects.create(
            user=request.user,
            status="Processing",
            total_price=final_cost,
            payment_method=payment_method,
            shipping_address=shipping_address,
            shipping_pincode=shipping_pincode,
            shipping_phone_number=shipping_phone_number,
            shipping_state=shipping_state,
            is_paid=False,
            coupon_applied=coupon_applied,
            coupon=coupon,
            discount_amount=discount,
            razorpay_order_id=razorpay_order['id']
        )
        if coupon:
            CouponUsage.objects.create(
                coupon=coupon,
                user=request.user,
                order=order
            )
        try:
            del request.session['applied_coupon']
            del request.session['discount']
            del request.session['total_cost']
        except KeyError:
            pass
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.new_price
            )   
        #     item.product.stock -= item.quantity
        #     item.product.save()
        # cart_items.delete()
        order.save()
        
        context = {
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key': settings.RAZORPAY_API_KEY,
            'amount': final_cost * 100,  
            'currency': "INR",
            'order_id': order.id
        }
        return JsonResponse(context)
    else:
        messages.warning(request, 'Something went wrong.')
        return redirect(request.META.get('HTTP_REFERER', 'checkout_page'))
    


def continue_payment(request,order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
            'razorpay_order_id': order.razorpay_order_id,
            'razorpay_key': settings.RAZORPAY_API_KEY,
            'amount': order.total_price * 100,  
            'currency': "INR",
            'order_id': order.id
        }
    return JsonResponse(context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        try:
           
            params = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            razorpay_client.utility.verify_payment_signature(params)

            order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)
            order.is_paid = True
            order.status = "Pending"
            order.save()

            cart_items = CartItem.objects.filter(cart__user=request.user)
            for item in cart_items:
                item.product.stock -= item.quantity
                item.product.save()
            cart_items.delete()

            return JsonResponse({
                "success": True,
                "order_id": order.id,
                "message": "Payment verified successfully."
            })

        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'success': False, 'message': 'Payment verification failed.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})







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
    final_price = order.total_price
    
    discount_amount = order.discount_amount
    total_cost=0
    for item in order_items:
        total_cost += item.price * item.quantity
    
    return render(request, 'order_detail.html', {
        'order': order,
        'order_items': order_items,
        'total_cost': total_cost,
        'discount_amount': discount_amount,
        'final_price': final_price
    })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def generate_invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    
    context = {
        'invoice_title': "INVOICE",
        'invoice_number': f"INV-{order.id}",
        'invoice_date': timezone.now().date(),
        'customer_name': f"{order.user.first_name} {order.user.last_name}",
        'customer_address': order.shipping_address,
        'customer_contact': order.shipping_phone_number,
        'order_number': order.id,
        'order_date': order.order_date,
        'payment_method':order.payment_method,
        'delivery_date': order.delivery_date,
        'products': [
            {
                'description': item.product.name,
                'quantity': item.quantity,
                'unit_price': item.price,
                'total_price': item.quantity * item.price,
            }
            for item in order_items
        ],
        'subtotal': sum(item.quantity * item.price for item in order_items),
        'delivery_charge': 100,  
        'discounts': order.discount_amount,
        'grand_total': order.total_price,
        'terms': "Products can be returned within 7 days if unopened.",
        'thank_you_message': "Thank you for shopping with us!",
    }

    html = render_to_string('invoice_template.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'
    pdf = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=pdf)

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    response.write(pdf.getvalue())
    pdf.close()
    return response




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'Cancelled':
        order.status = 'Cancelled'
        order.save()

        if order.payment_method == 'Razorpay' and order.is_paid:
            wallet, created = Wallet.objects.get_or_create(user=request.user)
            refund_amount = order.total_price
            wallet.credit(refund_amount)
            messages.success(request, f"Order cancelled and ${refund_amount} refunded to your wallet!")


        for item in order.order_items.all():  
            item.product.stock += item.quantity
            item.product.save()
        messages.success(request, "Order cancelled!")
    return redirect('my_orders')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def order_success(request,order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.order_items.all()
    return render(request, 'order_success_page.html',{
        'order': order,
        'order_items': order_items
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def return_order(request,order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'Delivered':
        order.status = 'Return'
        order.return_date = order.delivery_date + timedelta(days=7)
        order.save()
        messages.success(request, "Applied for return of order.")
    else:
        messages.error(request, "unexpected error")

    return redirect('order_detail' ,order.id)


def failed_payment(request,order_id):
    order = Order.objects.get(id=order_id)
    return render(request,'failed_payment_page.html',{'order':order})
