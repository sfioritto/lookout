from django.conf.urls.defaults import *
from webapp import settings

urlpatterns = patterns('webapp.blurb.views',
                       (r'(?P<blurbid>[0-9]+)/visit/', 'visit'),
                       (r'(?P<blurbid>[0-9]+)/reject/', 'reject'),
                       )

