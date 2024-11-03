
from django.urls import path
from . import views


urlpatterns = [

    path('admin_login/', views.custom_admin_login, name='custom_admin_login'),
    path('admin_logout/', views.custom_admin_logout, name='custom_admin_logout'),

    path('adminhome/',views.admin_home,name='admin_home'),
    path('adminhome/userlist/', views.user_list, name='user_list'),
    path('adminhome/userlist/userdetails/<int:user_id>/', views.user_detail, name='user_detail'),

    path('adminhome/categorylist/', views.category_list, name='category_list'),
    path('adminhome/categorylist/add/', views.category_add, name='category_add'),
    path('adminhome/categorylist/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('adminhome/categorylist/restore/<int:pk>/', views.category_restore, name='category_restore'),
    path('adminhome/categorylist/editcategory/<int:category_id>/', views.edit_category, name='edit_category'),

    path('adminhome/productlist/', views.product_list, name='product_list'),
    path('adminhome/productlist/add/', views.add_product, name='add_product'),
    path('adminhome/productlist/edit/<int:product_id>/',views.edit_product, name='edit_product'),
    path('adminhome/productlist/delete/<int:product_id>/', views.soft_delete_product, name='soft_delete_product'),
    path('adminhome/productlist/restore/<int:product_id>/', views.restore_product, name='restore_product'),
    path('adminhome/productlist/delete/<int:product_id>/', views.delete_product, name='delete_product'),
] 