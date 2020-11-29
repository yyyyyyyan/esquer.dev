from django.urls import path
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from . import feeds
from . import views

urlpatterns = [
    path(
        "termos-de-uso/", TemplateView.as_view(template_name="terms.html"), name="terms"
    ),
    path(
        "politica-de-privacidade/",
        TemplateView.as_view(template_name="privacy.html"),
        name="privacy",
    ),
    path("sobre/", TemplateView.as_view(template_name="about.html"), name="about"),
    path(
        "contato/", TemplateView.as_view(template_name="contact.html"), name="contact"
    ),
    path("", views.PostList.as_view(), name="post_list"),
    path("posts/", RedirectView.as_view(pattern_name="post_list", permanent=True)),
    path("posts/feed/", feeds.PostsFeed(), name="posts_rss"),
    path("posts/<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path("tags/<keyword>/", views.PostListByTag.as_view(), name="search_keyword"),
]
