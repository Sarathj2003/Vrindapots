
from django.urls import path
from . import views


urlpatterns = [
    path('adminhome/',views.admin_home,name='admin_home'),
    path('adminhome/userlist/', views.user_list, name='user_list'),
    path('adminhome/userlist/userdetails/<int:user_id>/', views.user_detail, name='user_detail'),

    path('adminhome/categorylist/', views.category_list, name='category_list'),
    path('adminhome/categorylist/add/', views.category_add, name='category_add'),
    path('adminhome/categorylist/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('adminhome/categorylist/restore/<int:pk>/', views.category_restore, name='category_restore'),
    path('adminhome/categorylist/editcategory/<int:category_id>/', views.edit_category, name='edit_category'),
] 
