from .models import Client, Message, Mailing, Attempt
from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'views')
    search_fields = ('title',)
    list_filter = ('published_date',)

# Register your models here.

admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Mailing)
admin.site.register(Attempt)

