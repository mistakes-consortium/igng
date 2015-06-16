from django import template
from django.conf import settings

register = template.Library()

BASE = settings.SITE_URL
@register.simple_tag
def g_markdown(image, title):
    z= dir(image)
    out = "[%s](%s%s)" % (title, BASE, image.file)
    return out

@register.simple_tag
def g_bb(image, title):
    out = "[img]%s%s[/img]" % (BASE,image.url,)
    return out

@register.simple_tag
def g_bb_linked(image, title):
    out = "[url=%s%s][img]%s%s[/img][/url]" % (BASE, image.url, BASE, image.url)
    return out

@register.simple_tag
def g_html(image, title):
    out = '<pre><a href="%s%s" title="%s">%s</img></a></pre>' % (BASE, image.url, title, title)
    return out