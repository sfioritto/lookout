import logging
from webapp.alerts.models import Alert
from app.model import alerts
from lamson.routing import route, stateless
from lamson import queue
from django.db import transaction

LOG = logging.getLogger("alertq")

@route('alerts-(alert_id)@(host)')
@stateless
@transaction.commit_manually
def START(message, alert_id=None, host=None):
    
    """
    This reads in the alert emails, parses them and
    sticks them in the database as blurbs.
    """
    
    try:
        alert = Alert.objects.get(pk=int(alert_id))
        if not alert.disabled:
            url = alerts.get_remove_url(message.body())
            LOG.debug("The removeurl for alert %s is %s" % (alert.id, url))
            if url:
                alert.removeurl = url
            else:
                q = queue.Queue("run/error")
                q.push(message)

            alert.save()
            alerts.create_blurbs(message, alert)
            transaction.commit()
        else:
            LOG.debug("Received alerts for a disabled alert with id %s and remove url %s" % (alert.id, alert.removeurl))

    except Exception as e:
        #queue up any messages that failed so we can diagnose
        #and try later.
        LOG.debug("Something bad happened with the alerts queue: %s" % str(e))
        transaction.rollback()
        q = queue.Queue("run/error")
        q.push(message)



