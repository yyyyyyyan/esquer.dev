from uuid import uuid4
from django.db import models
import readtime


class Post(models.Model):
    title = models.CharField(max_length=255)
    markdown = models.TextField()
    description = models.TextField()
    keywords = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    slug = models.SlugField(max_length=100)
    lock_key = models.CharField(max_length=32, blank=True)
    readtime = models.PositiveSmallIntegerField(editable=False)
    has_code = models.BooleanField(editable=False)

    def save(self, *args, **kwargs):
        self.keywords = ', '.join({keyword.strip() for keyword in self.keywords.split(',')})
        self.lock_key = self.lock_key if self.lock_key else uuid4().hex
        self.readtime = readtime.of_markdown(self.markdown, wpm=250).minutes
        self.has_code = "```" in self.markdown
        super(Post, self).save(*args, **kwargs)
