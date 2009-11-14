from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# FIXME: It would be much nicer to use an inclusion tag, but thats part of
# the django development branch, and isn't available to app engine yet...
@register.filter(name='list_beers')
def list_beers(beers, type):
    str = '<h2>' + type + ' Beers</h2><ul>'
    for beer in beers:
        key = "%s" % beer.key()
        str += '<li><a href="/beer/' + key + '">' + beer.name + '</a></li>'
    str += '</ul>'
    return mark_safe(str)
