from django.shortcuts import render
from .models import Category,Product,Tag,Banner
from authentication.models import Customer
# Create your views here.

def home_page(request):

    Exclusive_Offer_products = Product.objects.filter(tag__name='Exclusive Offers')
    banner = Banner.objects.first()

    return render(request,'home.html',{'Exclusive_Offer_products': Exclusive_Offer_products,'banner': banner,})