
from django.urls import path
from . import views


urlpatterns = [
    path('home/',views.home_page,name='home'),
    path('all_products/',views.all_products_page,name='all_products'),
    path('category/<id>/',views.category_products_page, name='category_products'),
    path('tag/<id>/',views.tag_products_page, name='tag_products'),
    path('product_detail/<id>/',views.product_detail_view,name='product_detail'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    
] 
