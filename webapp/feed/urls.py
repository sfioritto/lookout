from django.conf.urls.defaults import *
from webapp import settings

urlpatterns = patterns('webapp.feed.views',
                       (r'^$', 'show'),
                       (r'ajax/$', 'show_ajax'),
                       (r'older', 'older'),
                       )
