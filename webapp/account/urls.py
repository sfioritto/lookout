from django.conf.urls.defaults import *
from webapp import settings

urlpatterns = patterns('webapp.account.views',
                       (r'create/$', 'create'),
                       (r'profile/$', 'profile'),
                       (r'profile/edit/$', 'edit_profile'),
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
    (r'^registration/reset/$', 'password_reset', {
            'template_name' : 'account/registration/password_reset_form.html'
            }),
    (r'^registration/reset/done/$', 'password_reset_done', {
            'template_name' : 'account/registration/password_reset_done.html'
            }),
    (r'^registration/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm', {
            'template_name' : 'account/registration/password_reset_confirm.html'
            }),
    (r'^registration/reset/complete/$', 'password_reset_complete', {
            'template_name' : 'account/registration/password_reset_complete.html'
            }),
    )

