from django.conf.urls.defaults import *
from mobile_app.views import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^$', Index),
    #(r'^update/(\d+)/(\d+)', Update),
    #(r'^beer/(.*)', BrewDetail),
    #(r'^search/*(.*)', Search),
    #(r'^cask/', CaskHandler),
    #(r'^can/', CanHandler),
    #(r'^bottle/', BottleHandler),
    #(r'^draft/', DraftHandler),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^smedia/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_MEDIA_URL, 'show_indexes' : True}),)
