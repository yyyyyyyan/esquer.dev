from django.db import models


class Post(models.Model):
    title = models.TextField()
    markdown = models.TextField()
    pub_date = models.DateTimeField()
    slug = models.SlugField()
    author = models.ForeignKey('Author', null=True, on_delete=models.SET_NULL)


class Author(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    url = models.URLField()