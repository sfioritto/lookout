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
    rejected = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)


    @property
    def text(self):
        text = self.blurb + self.title + self.source + self.byline + self.url
        return text

    @property
    def visit(self):
        return reverse("webapp.blurb.views.visit", kwargs={'clientid':self.client.id,
                                                           'blurbid':self.id})

    def reject_url(self):
        return reverse("webapp.blurb.views.reject", kwargs={'clientid':self.client.id,
                                                           'blurbid':self.id})   

    def approve_url(self):
        return reverse("webapp.blurb.views.reject", kwargs={'clientid':self.client.id,
                                                           'blurbid':self.id})   

    def approve(self):
        self.rejected = False
        self.approved = True
        self.relevant = True
        self.save()


    def reject(self):
        self.rejected = True
        self.approved = False
        self.relevant = False
        self.save()

    
    def __unicode__(self):
        return "%s" % self.id



