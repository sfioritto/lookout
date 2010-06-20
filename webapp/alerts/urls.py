from django.conf.urls.defaults import *
from webapp import settings

urlpatterns = patterns('webapp.alerts.views',
                       (r'^$', 'manage'),
                       (r'^list/', 'alert_list'),
                       (r'^create/', 'create'),
                       (r'^disable/', 'disable'),
                       )
