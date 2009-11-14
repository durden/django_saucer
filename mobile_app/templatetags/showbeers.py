from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# FIXME: It would be much nicer to use an inclusion tag, but thats part of
# the django development branch, and isn't available to app engine yet...
@register.filter(name='list_beers')
def list_beers(beers, type):
    str = '<h2>' + type + ' Beers</h2><ul>'
    for beer in beers:
        id = "%s" % beer.id
        str += '<li><a href="/beer/' + id + '">' + beer.name + '</a></li>'
    str += '</ul>'
    return mark_safe(str)
