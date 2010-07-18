from django.conf.urls.defaults import *
from webapp import settings

urlpatterns = patterns('webapp.account.views',
                       (r'create/$', 'create'),
                       )

#registration and authentication
urlpatterns += patterns(
    'django.contrib.auth.views',
    (r'^login/$', 'login', {
        'template_name': 'account/login.html'}
     ),
    (r'logout/$', 'logout_then_login'),
    (r'^registration/change/$', 'password_change', {
            'template_name' : 'account/registration/password_change_form.html'
            }),
    (r'^registration/change/done/$', 'password_change_done', {
            'template_name' : 'account/registration/password_change_done.html'
            }),
    (r'^registration/reset/$', 'password_reset'),
    (r'^registration/reset/done/$', 'password_reset_done'),
    (r'^registration/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    (r'^registration/reset/done/$', 'password_reset_complete'),
    )

