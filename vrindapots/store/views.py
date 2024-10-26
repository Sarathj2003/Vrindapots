from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Category,Product,Tag,Banner,Review,ProductImage
from django.db.models import F, ExpressionWrapper, FloatField, Avg, Count, Q, Value
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Coalesce
from django.db.models import Prefetch
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def home_page(request):
    banner = Banner.objects.first()

    Exclusive_Offer_products = Product.objects.filter(tag__name='Exclusive Offers',category__is_deleted=False).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        )
    ).prefetch_related(
    Prefetch('images', queryset=ProductImage.objects.filter(is_main=True), to_attr='main_image')
    )[:3]

    Best_Seller_products = Product.objects.filter(tag__name='Best Sellers',category__is_deleted=False).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        )
    ).prefetch_related(
    Prefetch('images', queryset=ProductImage.objects.filter(is_main=True), to_attr='main_image')
    )[:3]

    New_Arrivals_products = Product.objects.filter(tag__name='New Arrivals',category__is_deleted=False).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        )
    ).prefetch_related(
    Prefetch('images', queryset=ProductImage.objects.filter(is_main=True), to_attr='main_image')
    )[:3]

    Seasonal_Specials_products = Product.objects.filter(tag__name='Seasonal Specials',category__is_deleted=False).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        )
    ).prefetch_related(
    Prefetch('images', queryset=ProductImage.objects.filter(is_main=True), to_attr='main_image')
    )[:3]
    
    return render(request, 'home.html', {
        'banner': banner,
        'Exclusive_Offer_products': Exclusive_Offer_products,
        'Best_Seller_products': Best_Seller_products,
        'New_Arrivals_products': New_Arrivals_products,
        'Seasonal_Specials_products': Seasonal_Specials_products,
        
    })

def all_products_page(request):
    banner = Banner.objects.first()
    all_products = Product.objects.ilter(category__is_deleted=False).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'), 
        average_rating=Coalesce(Avg('reviews__rating'), Value(0, output_field=FloatField())),  
        rating_percentage=Coalesce(Avg('reviews__rating') * 20, Value(0, output_field=FloatField()))  
    ).prefetch_related(
    Prefetch('images', queryset=ProductImage.objects.filter(is_main=True), to_attr='main_image')
    )
    return render(request, 'all_products.html', {
        'banner': banner,
        'all_products': all_products,
    })

def category_products_page(request, id):
    banner = Banner.objects.first()
    category_name = Category.objects.filter(id=id).first()
    category_products = Product.objects.filter(category__id=id).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'),  
        average_rating=Coalesce(Avg('reviews__rating'), Value(0, output_field=FloatField())),  
        rating_percentage=Coalesce(Avg('reviews__rating') * 20, Value(0, output_field=FloatField()))  
    ).prefetch_related(
    Prefetch('images', queryset=ProductImage.objects.filter(is_main=True), to_attr='main_image')
    )
    return render(request, 'category_products.html', {
        'banner': banner,
        'category_products': category_products,
        'category_name' : category_name,
    })

def tag_products_page(request, id):
    banner = Banner.objects.first()
    tag_name = Tag.objects.filter(id=id).first()
    tag_products = Product.objects.filter(tag__id=id).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'),  
        average_rating=Coalesce(Avg('reviews__rating'), Value(0, output_field=FloatField())),  
        rating_percentage=Coalesce(Avg('reviews__rating') * 20, Value(0, output_field=FloatField()))  
    ).prefetch_related(
    Prefetch('images', queryset=ProductImage.objects.filter(is_main=True), to_attr='main_image')
    )
    return render(request, 'tag_products.html', {
        'banner': banner,
        'tag_products': tag_products,
        'tag_name' : tag_name,
    })


def product_detail_view(request, id):
   
    product = get_object_or_404(Product, id=id)
    main_image = product.images.filter(is_main=True).first()
   
    average_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = Review.objects.filter(product=product).count()
   
    reviews = Review.objects.filter(product=product).select_related('user').order_by('-created_at')
    rating_percentage = average_rating * 20

    related_products = Product.objects.filter(
        Q(category=product.category) & ~Q(id=product.id)
    ).annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'),  
        average_rating=Coalesce(Avg('reviews__rating'), Value(0,output_field=FloatField())),  
        rating_percentage=Coalesce(Avg('reviews__rating') * 20, Value(0,output_field=FloatField()))  
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
        'main_image': main_image,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'reviews': reviews,
        'rating_percentage': rating_percentage,
        'related_products' : related_products,
        
    }
    return render(request, 'product_detail.html', context)



# def add_review(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if request.method == 'POST':
#         rating = request.POST.get('rating')  
#         comment = request.POST.get('comment')

        
#         if Review.objects.filter(product=product, user=request.user).exists():
#             messages.error(request, 'You have already reviewed this product.')
#             return redirect('product_detail', product_id=product_id)

        
#         Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
#         messages.success(request, 'Your review has been added.')
#         return redirect('product_detail', product_id=product_id)

#     return render(request, 'add_review.html', {'product': product})