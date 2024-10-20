
from django.urls import path
from . import views


urlpatterns = [
    path('home/',views.home_page,name='home'),
    path('product_detail/<id>/',views.product_detail_view,name='product_detail'),
    path('product_detail2/<id>/',views.product_detail_view_2,name='product_detail2'),
    path('product_detail3/<id>/',views.product_detail_view_3,name='product_detail3'),
] 
