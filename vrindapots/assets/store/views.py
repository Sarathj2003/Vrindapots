from django.shortcuts import render
from .models import Category,Product,Tag,Banner
from authentication.models import Customer
from django.db.models import F, ExpressionWrapper, FloatField
# Create your views here.

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
    
    return render(request, 'home.html', {
        'banner': banner,
        'Exclusive_Offer_products': Exclusive_Offer_products,
        'Best_Seller_products': Best_Seller_products,
        
    })