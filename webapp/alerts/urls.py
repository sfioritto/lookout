from django.conf.urls.defaults import *
from webapp import settings

urlpatterns = patterns('webapp.alerts.views',
                       (r'^$', 'show'),
                       (r'create/', 'create'),
                       )
