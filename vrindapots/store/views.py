from django.shortcuts import render
from .models import Category,Product,Tag
from authentication.models import Customer
# Create your views here.

def home_page(request):

    Exclusive_Offer_products = Product.objects.filter(tag__name='Exclusive Offers')

    return render(request,'home.html',{'Exclusive_Offer_products': Exclusive_Offer_products})