from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta

# BlogPost model
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # For SEO-friendly URLs
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True)  # Comma-separated tags
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# OTP model for email verification with expiration logic
class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_time = models.DateTimeField(default=timezone.now)  # OTP expiry time

    def __str__(self):
        return f"OTP for {self.user.username}"

    def is_expired(self):
        return self.expiry_time < timezone.now()

    def save(self, *args, **kwargs):
        if not self.expiry_time:
            self.expiry_time = self.created_at + timedelta(minutes=10)  # OTP valid for 10 minutes
        super().save(*args, **kwargs)
