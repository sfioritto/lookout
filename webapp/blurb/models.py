from django.db import models
from webapp.clients.models import Client
from webapp.alerts.models import Alert

class Blurb(models.Model):
    
    created_on = models.DateTimeField(auto_now_add=True, auto_now=True)
    alert = models.ForeignKey(Alert)
    folder = models.ForeignKey(Client)
    byline = models.CharField(max_length=1024)
    source = models.CharField(max_length=1024)
    title = models.CharField(max_length=1024)
    blurb = models.CharField(max_length=2048)
    url = models.CharField(max_length=1024)
    
    def __unicode__(self):
        return "%s" % self.id

