from django.conf.urls.defaults import *
from webapp import settings

urlpatterns = patterns('webapp.account.views',
                       (r'create/$', 'create'),
                       )
