import clients.alerts as alerts
from lamson.routing import route, route_like
# from config.settings import relay, CONFIRM
# from lamson import view, queue
# from app.model import mailinglist
# from types import ListType
# from email.utils import parseaddr


@route('alerts-(alert_id)@(host)')
def START(message, alert_id=None, host=None):
    return CONFIRMING(*args, **kwargs)


@route_like(START)
def CONFIRMING(message, alert_id=None, host=None):

    """
    Waiting for an email with a confirmation link.
    """

    try:
        alerts.confirm_alert(message)
    except:
        q = queue.Queue("run/error")
        q.push(message)
    return ALERTING


@route_like(START)
def ALERTING(message, alert_id=None, host=None):

    """
    """

    return ALERTING
