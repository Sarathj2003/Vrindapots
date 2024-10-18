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