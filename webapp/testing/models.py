from django.db import models

class Confirmation(models.Model):

    created_on = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return "%s" % self.id



