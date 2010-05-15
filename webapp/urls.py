from webapp import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    (r'^alerts/', include('webapp.testing.urls')),
    (r'^folders/(?P<folderid>[0-9]+)/feed/', include('webapp.feed.urls')),
    (r'^login/$', 'django.contrib.auth.views.login', {
            'template_name': 'account/login.html'}),
    (r'logout/$', 'django.contrib.auth.views.logout_then_login'),
    )

#load static files when in dev.
if settings.TEMPLATE_DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),)

