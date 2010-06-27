from django.conf.urls.defaults import *
from webapp import settings

urlpatterns = patterns('',)
#add local google alerts handlers for testing
if settings.DEBUG:
    urlpatterns += patterns('webapp.testing.views',
                            (r'verify/bad', 'bad_verify'),
                            (r'verify', 'good_verify'),
                            (r'create', 'create'),
                            (r'disable/bad', 'bad_disable'),
                            (r'disable', 'good_disable'),
                     )
