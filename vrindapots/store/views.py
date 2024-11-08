from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Category,Product,Tag,Banner,Review,Wishlist,Cart,CartItem
from django.db.models import F, ExpressionWrapper, FloatField, Avg, Count, Q, Value
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Coalesce
from django.db.models import Prefetch
from django.contrib import messages
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

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, 'Product added to wishlist.')
    else:
        messages.error(request, 'Product is already in your wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))
    

def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist')  

def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart})



from django.shortcuts import redirect
from django.contrib import messages

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get the desired quantity from the request (default to 1 if not provided)
    quantity = int(request.POST.get("quantity", 1))

    # Check stock availability before creating or getting the cart item
    if product.stock < quantity:
        messages.error(request, "Not enough stock available.")
        return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))

    # Proceed only if there's enough stock
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        # If the item is new, set the quantity directly
        cart_item.quantity = quantity
    else:
        # If the item already exists, add the new quantity to the existing one
        if product.stock < cart_item.quantity + quantity:
            messages.error(request, "Not enough stock available.")
            return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))
        cart_item.quantity += quantity  # Add the requested quantity

    # Save the cart item and show a success message
    cart_item.save()
    messages.success(request, f"Added {quantity} of {product.name} to your cart.")
    
    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))




def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    messages.success(request, "Removed item from your cart.")
    return redirect('cart_detail')
    

