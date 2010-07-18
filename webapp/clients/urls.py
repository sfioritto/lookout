from django.conf.urls.defaults import *
from webapp import settings

urlpatterns = patterns('webapp.clients.views',
                       (r'^$', 'show'),
                       (r'create/$', 'create'),
                       (r'delete/$', 'delete'),
                       (r'update/$', 'update'),
                       )
