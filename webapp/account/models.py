from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=512, primary_key=True)
    user = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return "%s" % self.email


