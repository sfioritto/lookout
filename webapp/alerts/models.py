from django.db import models
from webapp.account.models import Account
from webapp.clients.models import Client

class Alert(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Account)
    client = models.ForeignKey(Client)
    term = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    frequency = models.CharField(max_length=256)
    length = models.IntegerField()
    confirmed = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)

    @property
    def email(self):
        return "alerts-%s@lookoutthere.com" % self.id

    @property
    def update(self):
        return "/"


class LamsonState(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=512)
    address = models.EmailField()
    state = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s:%s (%s)" % (self.key, self.address, self.state)

