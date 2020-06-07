from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='tools/tools.html'), name='tools'),
    path('removedor-metadados', views.remove_metadata, name='metadata-removal'),
]