from django.core.urlresolvers import reverse
from django.db import models
from webapp.account.models import Account

class Client(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Account)
    name = models.CharField(max_length=256, null=False)

    @property
    def feed(self):
        return reverse('webapp.feed.views.show', kwargs={'clientid':self.id})

    @property
    def manage(self):
        return reverse('webapp.alerts.views.manage', kwargs={'clientid':self.id})

    def all_alerts(self):
        return self.alert_set.filter(disabled=False).all()

    def __unicode__(self):
        return "%s" % self.id
