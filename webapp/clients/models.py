from django.core.urlresolvers import reverse
from django.db import models
from webapp.account.models import Account
from datetime import datetime as dt, timedelta as td


class Client(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Account)
    name = models.CharField(max_length=256, null=False)

    @property
    def feed(self):
        return reverse('webapp.feed.views.show', kwargs={'clientid':self.id})

    @property
    def manage(self):
        return reverse('webapp.alerts.views.manage', kwargs={'clientid':self.id})

    def all_alerts(self):
        return self.alert_set.filter(disabled=False).order_by('created_on').all()


    def older_blurbs(self, filters={'relevant' : True}):
        """
        Return all of the blurbs older than yesterday. Accepts an optional
        dictionary of filters based on blurb properties, default
        is {'relevant' : True}
        """
        yesterday = dt.today() - td(1)
        older = self.blurb_set.filter(created_on__lt=dt(yesterday.year,
                                                        yesterday.month,
                                                        yesterday.day))\
                                                        .filter(**filters)\
                                                        .order_by('-created_on')\
                                                        .all()
        return older

    def todays_blurbs(self, filters={'relevant' : True}):
        """
        Return all of the blurbs created today. Accepts an optional
        dictionary of filters based on blurb properties, default
        is {'relevant' : True}
        """
        today = dt.today()
        todays = self.blurb_set.filter(created_on__year=today.year,
                                       created_on__month=today.month,
                                       created_on__day=today.day)\
                                       .filter(**filters)\
                                       .order_by('-created_on')\
                                       .all()
        return todays

    def yesterdays_blurbs(self, filters=None):
        """
        Return all of the blurbs created yesterday. Accepts an optional
        dictionary of filters based on blurb properties, default
        is {'relevant' : True}
        """
        
        # filters are passed in, stored in preferences, or default to relevant=true.
        filters = filters or self.get_filters() or {'relevant' : True}
        yesterday = dt.today() - td(1)
        yesterdays = self.blurb_set.filter(created_on__year=yesterday.year,
                                           created_on__month=yesterday.month,
                                           created_on__day=yesterday.day)\
                                           .filter(**filters)\
                                           .order_by('-created_on')\
                                           .all()
        return yesterdays


    def get_filters(self):
        """
        Returns a dictionary of filters to be applied
        to any of the feed queries.
        """
        filters = dict([(p.key, p.value) for p in self.preferences_set.all()])
        return filters


    def __unicode__(self):
        return "%s" % self.id


class Preferences(models.Model):

    """
    Stores rows of key/value pairs which are used
    to store preferences for each client. TODO: get rid
    of this table and put this data as json in tokyo
    tyrant or memcached or something.
    """
    created_on = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client)
    key = models.CharField(max_length=256, unique=True)
    value = models.CharField(max_length=256)


    def __unicode__(self):
        return "{ '%s' : '%s' }" % (self.key, self.value)

