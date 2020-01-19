from django.db import models
import readtime


class Post(models.Model):
    title = models.CharField(max_length=255)
    markdown = models.TextField()
    description = models.TextField()
    keywords = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    slug = models.SlugField()
    readtime = models.PositiveSmallIntegerField(editable=False)
    has_code = models.BooleanField(editable=False)

    def save(self, *args, **kwargs):
        self.readtime = readtime.of_markdown(self.markdown, wpm=250).minutes
        self.has_code = "```" in self.markdown
        super(Post, self).save(*args, **kwargs)
