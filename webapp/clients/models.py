from django.db import models
from webapp.account.models import Account

class Client(models.Model):

    created_on = models.DateTimeField(auto_now_add=True, auto_now=True)
    user = models.ForeignKey(Account)
    name = models.CharField(max_length=256, null=False)

    def __unicode__(self):
        return "%s" % self.id