from django.db import models
from webapp.account.models import Account
from webapp.folders.models import Folder

class Alert(models.Model):

    created_on = models.DateTimeField(auto_now_add=True, auto_now=True)
    user = models.ForeignKey(Account)
    folder = models.ForeignKey(Folder)
    term = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    frequency = models.CharField(max_length=256)
    length = models.IntegerField()

    @property
    def email(self):
        return "alerts-%s@lookoutthere.com" % self.id


class LamsonState(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=512)
    address = models.EmailField()
    state = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s:%s (%s)" % (self.key, self.address, self.state)

