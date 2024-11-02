
from django.urls import path
from . import views


urlpatterns = [
    path('',views.user_login,name='user_login'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_signup/',views.user_signup,name='user_signup'),
    path('userprofile/',views.profile_view,name='user_profile'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp_for_password_reset/', views.verify_otp_for_password_reset, name='verify_otp_for_password_reset'),
    path('reset_password/', views.reset_password, name='reset_password'),

    path('account/', views.account_page, name='account_page'),
    path('set_current_address/<int:profile_id>/', views.set_current_address, name='set_current_address'),
    path('add_new_address/', views.add_new_address, name='add_new_address'),
    path('edit_address/<int:profile_id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:profile_id>/', views.delete_address, name='delete_address'),

] 
