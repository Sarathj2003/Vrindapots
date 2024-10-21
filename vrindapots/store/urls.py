
from django.urls import path
from . import views


urlpatterns = [
    path('home/',views.home_page,name='home'),
    path('all_products/',views.all_products_page,name='all_products'),
    path('category/<id>/',views.category_products_page, name='category_products'),
    path('tag/<id>/',views.tag_products_page, name='tag_products'),
    path('product_detail/<id>/',views.product_detail_view,name='product_detail'),
    
] 
