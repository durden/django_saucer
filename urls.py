from django.conf.urls.defaults import *
from mobile_app.views import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from mobile_app.feeds import NewBeersFeed, RetiredBeersFeed

# Feeds
feeds = {'new': NewBeersFeed, 'retired': RetiredBeersFeed}

urlpatterns = patterns('',
    ('^$', index),
    (r'^update/(\d+)/(\d+)', update),
    (r'^retire/', retire),
    (r'^beer/(.*)', brew_detail),
    (r'^search/*(.*)', search),
    (r'^new/', new),
    (r'^retired/', retired),
    (r'^cask/', cask),
    (r'^can/', can),
    (r'^bottle/', bottle),
    (r'^draft/', draft),

    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}, name='feeds'),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^smedia/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_MEDIA_URL, 'show_indexes' : True}),)
