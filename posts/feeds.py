from django.contrib.syndication.views import Feed
from django.utils import timezone
from .models import Post


class PostsFeed(Feed):
    title = "esquer.dev"
    link = "https://esquer.dev/posts/"
    description = "Um blog de tecnologia e política à esquerda."
    item_author_name = "yyyyyyyan"
    item_author_email = "contato@esquer.dev"
    item_author_link = "https://twitter.com/yyyyyyyan_"
    feed_url = "https://esquer.dev/posts/feed/"

    def items(self):
        return Post.objects.order_by("-pub_date")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return "https://esquer.dev/posts/" + item.slug

    def item_categories(self, item):
        return item.keywords.split(",")

    def item_pubdate(self, item):
        return item.pub_date

    def feed_copyright(self):
        current_year = timezone.now().year
        return "&copy; Copyright {}, esquer.dev".format(current_year)
