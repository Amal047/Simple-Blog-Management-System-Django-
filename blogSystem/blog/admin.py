from django.contrib import admin
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')

admin.site.register(BlogPost, BlogPostAdmin)


# Register your models here.
