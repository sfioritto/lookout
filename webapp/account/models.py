from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True)

    def active_clients(self):
        return self.client_set.filter(disabled=False).all()

    def __unicode__(self):
        return "%s" % self.user.email


