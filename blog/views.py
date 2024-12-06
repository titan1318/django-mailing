from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from blog.forms import PostForm
from blog.models import Post
from services import get_data_from_cache


class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return get_data_from_cache(Post)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_post'] = Post.objects.all()[:6]
        # последний пост
        context['latest_post'] = Post.objects.order_by('-created_at').first()
        # два избранных поста
        context['featured_posts'] = Post.objects.filter(is_published=True)[:2]
        return context


class PostAllListView(ListView):
    model = Post
    template_name = 'post/post_all.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        self.object.save()
        return self.object


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_update', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.number_of_views > 1:
            self.object.number_of_views -= 1
            self.object.save()
        return self.object


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_all')


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_all')
