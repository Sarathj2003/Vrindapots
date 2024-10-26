
from django.urls import path
from . import views


urlpatterns = [
    path('adminhome/',views.admin_home,name='admin_home'),
    path('adminhome/userlist/', views.user_list, name='user_list'),
    path('adminhome/userlist/userdetails/<int:user_id>/', views.user_detail, name='user_detail'),
] 
