from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^admin/', include(admin.site.urls)),
                       )


#add local google alerts handlers for testing
if settings.DEBUG:
    urlpatterns += patterns('webapp.testing.views',
                            (r'^alerts/verify', 'verify'),
                     )

#load static files when in dev.
if settings.TEMPLATE_DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),)

