from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('create-post/', views.create_post, name='create_post'),  # Create post page
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Post detail page
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),  # Edit post page
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),  # Delete post page
    path('login/', views.login_view, name='login'),  # Login page
    path('register/', views.register_view, name='register'),  # Register page
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),  # OTP verification page
    path('dashboard/', views.user_dashboard, name='dashboard'),  # User dashboard
    path('update-info/', views.update_user_info, name='update_user_info'),  # Update personal info
    path('logout/', views.logout_view, name='logout'),  # Logout page
]
