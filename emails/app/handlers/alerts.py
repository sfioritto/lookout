import app.model.alerts as alerts
import logging
from lamson import queue
from lamson.routing import route, route_like, state_key_generator
from email.utils import parseaddr
from webapp.alerts.models import Alert

LOG = logging.getLogger("alerts")

@state_key_generator
def module_and_listname(modulename, message):

    name, address = parseaddr(message['to'])
    return modulename + ':' + address.split("@")[0]


@route('alerts-(alert_id)@(host)')
def START(message, alert_id=None, host=None):
    return CONFIRMING(message, alert_id, host)


@route_like(START)
def CONFIRMING(message, alert_id=None, host=None):

    """
    Waiting for an email with a confirmation link.
    """
    try:
        queue.Queue('run/all').push(message)
        alert = Alert.objects.get(pk=alert_id)
        # google alerts sends alerts from a different address than the confirmation email. Lamson
        # state key includes the sender, so I have to add this extra piece.
        if alert.confirmed:
            LOG.debug("Alert for alert id %s was already confirmed." % alert_id)
            return ALERTING(message, alert_id=alert_id, host=host)
        alerts.confirm_alert(message)
        alert.confirmed = True
        alert.removeurl = alerts.get_remove_url(message.body())
        if not alert.removeurl:
            q = queue.Queue('run/error')
            q.push(message)
        alert.save()
        LOG.debug("The removeurl for alert %s is %s" % (alert.id, alert.removeurl))
        return ALERTING
    except Exception as e:
        q = queue.Queue('run/error')
        q.push(message)
        LOG.debug("Something bad happened in the alerts handler: %s" % str(e))
        return CONFIRMING


@route_like(START)
def ALERTING(message, alert_id=None, host=None):
    """
    Just dump the alert message into a queue
    for later processing.
    """
    q = queue.Queue("run/alerts")
    q.push(message)
    queue.Queue("run/all").push(message)
    
    return ALERTING
