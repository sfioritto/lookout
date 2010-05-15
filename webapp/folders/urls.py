from django.conf.urls.defaults import *
from webapp import settings

urlpatterns = patterns('webapp.folders.views',
                       (r'', 'show'),
                       )
