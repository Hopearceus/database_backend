from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import UserProfileUpdateView

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.fetch_user_account_and_permissions, name='fetch_user_account_and_permissions'),
    path('profile/get/', views.get_user_profile, name='get_user_profile'),
    path('profile/put/', views.update_user_profile, name='update_user_profile'),
    path('profile/avatar/', views.upload_avatar, name='upload_avatar'),
]
