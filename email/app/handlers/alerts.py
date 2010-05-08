import clients.alerts as alerts
from lamson import queue
from lamson.routing import route, route_like, state_key_generator
from email.utils import parseaddr


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
        alerts.confirm_alert(message)
        return ALERTING
    except:
        q = queue.Queue('run/error')
        q.push(message)
        return CONFIRMING


@route_like(START)
def ALERTING(message, alert_id=None, host=None):

    """
    """

    return ALERTING
