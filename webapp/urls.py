from webapp import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

#webapp
urlpatterns = patterns(
    'webapp',
    (r'^admin/', include(admin.site.urls)),
    (r'^alerts/', include('testing.urls')),
    (r'^account/', include('account.urls')),
    (r'^clients/(?P<clientid>[0-9]+)/alerts/', include('alerts.urls')),
    (r'^clients/(?P<clientid>[0-9]+)/feed/', include('feed.urls')),
    (r'^clients/(?P<clientid>[0-9]+)/blurb/', include('blurb.urls')),
    (r'^clients/', include('clients.urls')),
    )

#generic
urlpatterns += patterns(
    'django.views.generic.simple',
    (r'^$', 'redirect_to', {'url' : settings.LOGIN_REDIRECT_URL}, 'home'),
    (r'^help/faq/$', 'direct_to_template', {'template' : 'help/faq.html'}, 'faq'),
    (r'^help/contact/$', 'direct_to_template', {'template' : 'help/contact.html'}, 'contact'),
    )

#load static files when in dev.
if settings.TEMPLATE_DEBUG:
    urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),)

