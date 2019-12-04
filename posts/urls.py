from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('termos-de-uso', TemplateView.as_view(template_name='terms.html'), name='terms'),
    path('politica-de-privacidade', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('contato', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('', views.PostList.as_view(), name='index'),
    path('posts/<slug:slug>', views.PostDetail.as_view(), name='detail')
]