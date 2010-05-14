from nose.tools import *
from lamson.testing import *
from lamson.routing import Router
from lamson.mail import MailRequest
from lamson import queue
from config import testing
from conf import email, home
from webapp.folders.models import Folder
from django.contrib.auth.models import User
from webapp.account.models import LamsonState, Account
from webapp.alerts.models import Alert
import os
import app.model.alerts as alerts

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
    user = User.objects.all()[0]
    account = Account(email="test@test.com",
                   user=user)
    account.save()
    folder = Folder(name="Beth",
                    user=account)
    folder.save()

    LamsonState.objects.all().delete()
    q = queue.Queue(email('run/error'))
    q.clear()
    q = queue.Queue(email('run/alerts'))
    q.clear()



def teardown_func():
    Alert.objects.all().delete()
    Account.objects.all().delete()
    Folder.objects.all().delete()

@with_setup(setup_func, teardown_func)
def test_good_confirmation():

    """
    This message should move the state into
    ALERTING.
    """

    Router.deliver(goodmsg)
    q = queue.Queue(email('run/alerts'))
    assert q.count() == 0
    assert_in_state('app.handlers.alerts', goodmsg['to'], sender, 'ALERTING') 


@with_setup(setup_func, teardown_func)
def test_bad_confirmation():
    Router.deliver(badmsg)
    q = queue.Queue(email('run/error'))
    assert q.count() == 2 #one for the alertsq module and one for alerts
    assert_in_state('app.handlers.alerts', badmsg['to'], sender, 'CONFIRMING') 


@with_setup(setup_func, teardown_func)
def test_incoming_alert():
    """
    Verify an incoming alert generates
    the correct database records.
    """
    alert = Alert(user=Account.objects.all()[0],
                  folder=Folder.objects.all()[0],
                  term="l",
                  type="l",
                  frequency="50",
                  length=50)
    alert.save()
    msg = MailRequest('fakepeer', sender, "alerts-%s@lookoutthere.com" % alert.id, open(home("tests/data/emails/alert-confirmation.msg")).read())
    msg['to'] = "alerts-%s@lookoutthere.com" % alert.id
    Router.deliver(msg)
    q = queue.Queue(email('run/error'))
    assert q.count() == 0

