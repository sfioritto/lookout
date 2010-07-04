from django.db import models
from django.core.urlresolvers import reverse
from webapp.clients.models import Client
from webapp.alerts.models import Alert

    
class Blurb(models.Model):
    
    created_on = models.DateTimeField(auto_now_add=True)
    alert = models.ForeignKey(Alert)
    client = models.ForeignKey(Client)
    byline = models.CharField(max_length=1024, blank=True)
    source = models.CharField(max_length=1024, blank=True)
    title = models.CharField(max_length=1024)
    blurb = models.CharField(max_length=2048)
    url = models.CharField(max_length=1024)
    visited = models.BooleanField(default=False)
    relevant = models.BooleanField(default=True)


    @property
    def text(self):
        text = self.blurb + self.title + self.source + self.byline + self.url
        return text

    @property
    def visit(self):
        return reverse("webapp.blurb.views.visit", kwargs={'clientid':self.client.id,
                                                           'blurbid':self.id})

    @property
    def relevance(self):
        return reverse("webapp.blurb.views.relevance", kwargs={'clientid':self.client.id,
                                                           'blurbid':self.id})

    
    def __unicode__(self):
        return "%s" % self.id



