from django.db import models
from webapp.account.models import User
from webapp.folders.models import Folder

class Alert(models.Model):

    created_on = models.DateTimeField(auto_now_add=True, auto_now=True)
    user = models.ForeignKey(User)
    folder = models.ForeignKey(Folder)
    term = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    email = models.CharField(max_length=512)
    frequency = models.CharField(max_length=256)
    length = models.IntegerField()


    
