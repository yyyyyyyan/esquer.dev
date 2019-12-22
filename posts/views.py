from django.views.generic import ListView, DetailView
from .models import Post


class PostDetail(DetailView):
    template_name = 'posts/post.html'
    context_object_name = 'post'
    model = Post

    def get_object(self, *args, **kwargs):
        post_object = super(PostDetail, self).get_object(*args, **kwargs)
        post_object.list_keywords = post_object.keywords.split(',')
        return post_object


class PostList(ListView):
    template_name = 'posts/post-list.html'
    context_object_name = 'posts'
    model = Post
    ordering = '-pub_date'
    paginate_by = 1


class PostListByTag(PostList):
    def get_queryset(self):
        queryset = self.model.objects.filter(keywords__icontains=self.kwargs['keyword']).order_by(self.ordering)
        return queryset
    
    def get_context_data(self, *args, **kwargs):
        context = super(PostListByTag, self).get_context_data(*args, **kwargs)
        context['keyword'] = self.kwargs['keyword']
        return context

# TODO: paginação