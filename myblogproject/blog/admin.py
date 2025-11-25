# blog/admin.py

from django.contrib import admin
from .models import Post, Comment, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'category')
    list_filter = ('pub_date', 'author', 'category')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'post', 'created_on', 'active') 
    search_fields = ('user__username', 'body') 
    list_filter = ('active', 'created_on')
    actions = ['approve_comments'] 

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Mark selected comments as approved"