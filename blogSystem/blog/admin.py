from django.contrib import admin
from .models import BlogPost

# Optimized BlogPost admin configuration
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
    list_per_page = 10  # Display 10 posts per page

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'image', 'tags', 'author')
        }),
    )

admin.site.register(BlogPost, BlogPostAdmin)

# Register your models here.
