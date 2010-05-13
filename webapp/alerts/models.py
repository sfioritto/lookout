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


class Blurb(models.Model):
    
    created_on = models.DateTimeField(auto_now_add=True, auto_now=True)
    alert = models.ForeignKey(Alert)
    folder = models.ForeignKey(Folder)
    byline = models.CharField(max_length=1024)
    source = models.CharField(max_length=1024)
    title = models.CharField(max_length=1024)
    blurb = models.CharField(max_length=2048)
    url = models.CharField(max_length=1024)




    
