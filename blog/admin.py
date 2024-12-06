from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'number_of_views', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'content',)
