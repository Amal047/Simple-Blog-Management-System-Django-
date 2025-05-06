from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, OTPVerification
from .forms import BlogPostForm, CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
import random

# Helper function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Index page with search functionality
def index(request):
    query = request.GET.get("q", "")
    posts = BlogPost.objects.all().order_by('-created_at')
    if query:
        posts = posts.filter(title__icontains=query)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/index.html', {'posts': page_obj})

# Post detail page
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/postDetails.html', {'post': post})

# Create new blog post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your post has been created successfully!")
            return redirect('index')
        else:
            messages.error(request, "There was an error with your form. Please check.")
    else:
        form = BlogPostForm()

    return render(request, 'blog/createPost.html', {'form': form})

# Edit existing blog post
@login_required
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect('dashboard')
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'blog/editPost.html', {'form': form, 'post': post})

# Delete blog post
@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    post.delete()
    messages.success(request, "Your post has been deleted successfully.")
    return redirect('dashboard')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin-dashboard/')  # Redirect to custom admin page
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'blog/login.html')

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Make user inactive until OTP verification
            user.save()

            otp = generate_otp()  # Generate OTP
            OTPVerification.objects.create(user=user, otp=otp)

            send_mail(
                'Your OTP Verification Code',
                f'Your OTP is {otp}',
                'your-email@gmail.com',
                [user.email],
                fail_silently=False,
            )

            request.session['uid'] = user.id  # Save user id in session for later use
            return redirect('verify_otp')  # Redirect to OTP verification page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form})

# OTP Verification view
def verify_otp_view(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('register')  # If no session found, redirect to registration

    user = User.objects.get(id=uid)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')  # Get OTP entered by user
        verification = OTPVerification.objects.get(user=user)

        if verification.otp == entered_otp:
            user.is_active = True  # Activate the user after OTP verification
            user.save()
            verification.delete()  # Delete OTP record after successful verification
            login(request, user)  # Log the user in
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'blog/verify_otp.html')

# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')

# User dashboard
@login_required
def user_dashboard(request):
    posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/dashboard.html', {'posts': posts})

# Update personal info
@login_required
def update_user_info(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # Handle password change if both fields are filled
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 and password2 and password1 == password2:
                user.set_password(password1)

            user.save()
            messages.success(request, "Your information has been updated. Please log in again if your password was changed.")
            login(request, user)  # Re-login the user if password changed
            return redirect('dashboard')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'blog/updateUserInfo.html', {'form': form})

# Admin dashboard view (only for superuser)
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('index')  # Redirect to index if user is not superuser

    # Get all users and their blog posts
    users = User.objects.all()
    blog_posts = BlogPost.objects.all().order_by('-created_at')

    paginator = Paginator(blog_posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/admin_dashboard.html', {'users': users, 'blog_posts': page_obj})

@login_required
def admin_view_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('index')
    
    user = get_object_or_404(User, id=user_id)
    posts = BlogPost.objects.filter(author=user)

    return render(request, 'blog/admin_view_user.html', {'user_obj': user, 'posts': posts})

@login_required
@require_POST
def delete_user_view(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only admins can delete users.")

    user_to_delete = get_object_or_404(User, id=user_id)

    if user_to_delete == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('admin-view-user', user_id=user_id)

    if user_to_delete.is_superuser:
        messages.error(request, "You cannot delete another admin user.")
        return redirect('admin-view-user', user_id=user_id)

    user_to_delete.delete()
    messages.success(request, "User has been deleted successfully.")
    return redirect('admin-dashboard')

# Revoke/Delete a blog post (only for superuser)
@login_required
def revoke_blog_post(request, post_id):
    if not request.user.is_superuser:
        return redirect('index')  # Redirect if not a superuser

    post = get_object_or_404(BlogPost, id=post_id)
    post.delete()
    messages.success(request, "Blog post has been revoked (deleted).")
    return redirect('admin-dashboard')
