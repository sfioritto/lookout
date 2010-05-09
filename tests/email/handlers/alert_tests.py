from nose.tools import *
from lamson.testing import *
from lamson.routing import Router
from lamson.mail import MailRequest
from lamson import queue
from config import testing
from conf import email, home
from webapp.account.models import LamsonState
import os
import clients.alerts as alerts

relay = relay(port=8823)
client = RouterConversation("somedude@localhost", "alerts_tests")
sender = "test@localhost"

goodmsg = MailRequest('fakepeer', sender, "alerts-1@lookoutthere.com", open(home("tests/data/emails/alert-confirmation.msg")).read())
goodmsg['to'] = "alerts-1@lookoutthere.com"

badmsg = MailRequest('fakepeer', sender, "alerts-2@lookoutthere.com", open(home("tests/data/emails/bad-confirmation.msg")).read())
badmsg['to'] = "alerts-2@lookoutthere.com"

#send the alerts urls to localhost
alerts.GOOGLE_URL = "localhost:8000"


def setup_func():
    LamsonState.objects.all().delete()
    q = queue.Queue(email('run/error'))
    q.clear()


def teardown_func():
    pass

@with_setup(setup_func, teardown_func)
def test_good_confirmation():

    """
    This message should move the state into
    ALERTING.
    """

    Router.deliver(goodmsg)
    q = queue.Queue(email('run/error'))
    assert q.count() == 0
    assert_in_state('app.handlers.alerts', goodmsg['to'], sender, 'ALERTING') 


@with_setup(setup_func, teardown_func)
def test_bad_confirmation():
    Router.deliver(badmsg)
    q = queue.Queue(email('run/error'))
    assert q.count() == 1
    assert_in_state('app.handlers.alerts', badmsg['to'], sender, 'CONFIRMING') 


@with_setup(setup_func, teardown_func)
def test_incoming_alert():
    """
    Verify an incoming alert generates
    the correct database records.
    """
    assert True



