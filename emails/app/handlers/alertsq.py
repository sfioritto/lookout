from webapp.alerts.models import Alert
from app.model import alerts
from lamson.routing import route, stateless
from lamson import queue
from django.db import transaction

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
        alerts.create_blurbs(message, alert)
        transaction.commit()

    except:
        #queue up any messages that failed so we can diagnose
        #and try later.
        transaction.rollback()
        q = queue.Queue("run/error")
        q.push(message)



