from django.conf.urls.defaults import *
from webapp import settings

urlpatterns = patterns('webapp.feed.views',
                       (r'^$', 'show'),
                       (r'older', 'older'),
                       (r'beta', 'login_redirect'),
                       )
