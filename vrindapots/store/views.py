
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
            coupon = Coupon.objects.get(code=coupon_code, is_active=True, start_date__lte=timezone.now(), end_date__gte=timezone.now())
            usage_count = CouponUsage.objects.filter(coupon=coupon, user=request.user).count()
            if coupon.per_user_limit is not None and usage_count >= coupon.per_user_limit:
                messages.error(request, "You have already used this coupon.")
                return redirect('cart_detail')
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

    return render(request, 'checkout_page.html', {
        'full_name': full_name,
        'profile': profile,
        'cart_items': cart_items,
        'total_cost': math.ceil(total_cost),
        'subtotal_cost': subtotal_cost,
        'profiles': profiles,
        'applied_coupon': request.session.get('applied_coupon', None),
        'wallet_balance': wallet.balance,
        
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
            item.product.stock -= item.quantity
            item.product.save()
        cart_items.delete()
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
            order.status = "Completed"
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

    