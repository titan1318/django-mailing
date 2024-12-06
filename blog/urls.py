from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.apps import BlogConfig
from blog.views import PostListView, PostDetailView, PostAllListView, PostUpdateView, PostDeleteView, PostCreateView

app_name = BlogConfig.name

urlpatterns = [
                  path('', PostListView.as_view(), name='post_list'),
                  path('post/list', PostAllListView.as_view(), name='post_all'),
                  path('post/<int:pk>/detail', PostDetailView.as_view(), name='post_detail'),
                  path('post/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
                  path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
                  path('post/create', PostCreateView.as_view(), name='post_create'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
