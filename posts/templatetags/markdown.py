from django import template
from markdown import markdown as markdown_text

register = template.Library()


@register.filter()
def markdown(value):
    return markdown_text(value, extensions=['fenced_code'])
