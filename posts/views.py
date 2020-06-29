from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from ratelimit.mixins import RatelimitMixin
from ratelimit import ALL as ALL_METHODS
from .models import Post


class PostDetail(RatelimitMixin, DetailView):
    ratelimit_key = "ip"
    ratelimit_rate = "10/m"
    ratelimit_method = ALL_METHODS

    template_name = 'posts/post.html'
    context_object_name = 'post'
    model = Post

    def get_queryset(self):
        queryset = super(PostDetail, self).get_queryset().filter(pub_date__lte=timezone.now())
        return queryset

    def get_object(self, *args, **kwargs):
        key = self.request.GET.get("key")
        if key:
            post_object = get_object_or_404(self.model, slug=self.kwargs["slug"], lock_key=key)
        else:
            post_object = super(PostDetail, self).get_object(*args, **kwargs)
        post_object.list_keywords = post_object.keywords.split(', ')
        return post_object


class PostList(RatelimitMixin, ListView):
    ratelimit_key = "ip"
    ratelimit_rate = "10/m"
    ratelimit_method = ALL_METHODS

    template_name = 'posts/post-list.html'
    context_object_name = 'posts'
    model = Post
    ordering = '-pub_date'
    paginate_by = 7

    def get_queryset(self):
        queryset = self.model.objects.filter(pub_date__lte=timezone.now()).order_by(self.ordering)
        return queryset


class PostListByTag(PostList):
    def get_queryset(self):
        queryset = super(PostListByTag, self).get_queryset().filter(keywords__icontains=self.kwargs['keyword'])
        return queryset
    
    def get_context_data(self, *args, **kwargs):
        context = super(PostListByTag, self).get_context_data(*args, **kwargs)
        context['keyword'] = self.kwargs['keyword']
        return context
