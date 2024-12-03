
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
    path('cart/update_quantity/<int:item_id>/', views.update_cart_item_quantity, name='update_cart_item_quantity'),

    path('checkout-page/', views.checkout, name='checkout_page'),

    path('placeorderCOD/', views.place_order_cod, name='place_order_cod'),
    path('placeorderWallet/', views.place_order_wallet, name='place_order_wallet'),
    path('placeorderRazorpay/', views.place_order_razorpay, name='place_order_razorpay'),

    # path('place-order/', views.place_order, name='place_order'), 
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/invoice/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/return/<int:order_id>/', views.return_order, name='return_order'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('order/verify_payment', views.verify_payment, name='verify_payment'),

 
    
    
] 
