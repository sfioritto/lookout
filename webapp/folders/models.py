from django.db import models
from webapp.account.models import User

class Folder(models.Model):

    created_on = models.DateTimeField(auto_now_add=True, auto_now=True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=256, null=False)

