from django import template
from markdown import Markdown

register = template.Library()
md = Markdown(extensions=["fenced_code", "toc"])


@register.filter()
def markdown(value):
    return md.convert(value)
