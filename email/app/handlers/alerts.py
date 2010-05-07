import clients.alerts as alerts
from lamson import queue
from lamson.routing import route, route_like
from settings import *


@route('alerts-(alert_id)@(host)')
def START(message, alert_id=None, host=None):
    return CONFIRMING(message, alert_id, host)


@route_like(START)
def CONFIRMING(message, alert_id=None, host=None):

    """
    Waiting for an email with a confirmation link.
    """

    try:
        alerts.confirm_alert(message)
    except:
        q = queue.Queue(LOOKOUT_ERROR)
        q.push(message)
    return ALERTING


@route_like(START)
def ALERTING(message, alert_id=None, host=None):

    """
    """

    return ALERTING
