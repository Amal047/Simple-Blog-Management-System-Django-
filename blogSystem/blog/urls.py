from django.urls import path
from . import views

urlpatterns = [
    # Home and General Blog Views
    path('', views.index, name='index'),
    path('create-post/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),

    # User Dashboard and Info
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('update-info/', views.update_user_info, name='update_user_info'),

    # Admin Functions
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin-view-user/<int:user_id>/', views.admin_view_user, name='admin-view-user'),
    path('delete-user/<int:user_id>/', views.delete_user_view, name='delete-user'),
    path('revoke-blog/<int:post_id>/', views.revoke_blog_post, name='revoke-blog'),
]
