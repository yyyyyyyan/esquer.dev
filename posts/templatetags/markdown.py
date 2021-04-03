from django import template
from markdown import Markdown

register = template.Library()
md = Markdown(
    extensions=["fenced_code", "codehilite", "toc"],
    extension_configs={"codehilite": {"linenums": False, "guess_lang": False}},
    output_format="html5",
)


@register.filter()
def markdown(value):
    return md.convert(value)
