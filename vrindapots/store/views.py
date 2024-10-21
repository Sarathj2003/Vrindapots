from django.shortcuts import render
from .models import Category,Product,Tag,Banner
from django.db.models import F, ExpressionWrapper, FloatField
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def home_page(request):
    banner = Banner.objects.first()

    Exclusive_Offer_products = Product.objects.filter(tag__name='Exclusive Offers').annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        )
    )
    Best_Seller_products = Product.objects.filter(tag__name='Best Sellers').annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        )
    )
    New_Arrivals_products = Product.objects.filter(tag__name='New Arrivals').annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        )
    )
    Seasonal_Specials_products = Product.objects.filter(tag__name='Seasonal Specials').annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        )
    )
    
    return render(request, 'home.html', {
        'banner': banner,
        'Exclusive_Offer_products': Exclusive_Offer_products,
        'Best_Seller_products': Best_Seller_products,
        'New_Arrivals_products': New_Arrivals_products,
        'Seasonal_Specials_products': Seasonal_Specials_products,
        
    })

def all_products_page(request):
    banner = Banner.objects.first()
    all_products = Product.objects.all().annotate(
        discount=ExpressionWrapper(
            (F('old_price') - F('new_price')) * 100 / F('old_price'),
            output_field=FloatField()
        )
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
        )
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
        )
    )
    return render(request, 'tag_products.html', {
        'banner': banner,
        'tag_products': tag_products,
        'tag_name' : tag_name,
    })


def product_detail_view(request, id):
    product = Product.objects.get(id=id)

    context = {
        'product': product,
    }

    return render(request, 'product_detail.html', context)

