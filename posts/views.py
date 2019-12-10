from django.views.generic import ListView, DetailView
from .models import Post


class PostDetail(DetailView):
    template_name = 'posts/post.html'
    context_object_name = 'post'
    model = Post

    def get_object(self, *args, **kwargs):
        object = super(PostDetail, self).get_object(*args, **kwargs)
        object.keywords = object.keywords.split(',')
        return object


class PostList(ListView):
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    model = Post
    ordering = ['-pub_date']

# TODO: paginação