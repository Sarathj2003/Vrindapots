
from django.urls import path
from . import views


urlpatterns = [
    path('home/',views.home_page,name='home'),
    path('product_detail/<id>/',views.product_detail_view,name='product_detail'),
    
] 
