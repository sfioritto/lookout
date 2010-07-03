from tests.email import create_alert
from nose.tools import *
from lamson.testing import *
from lamson.routing import Router
from lamson.mail import MailRequest
from lamson import queue
from config import testing
from conf import email, home
from webapp.clients.models import Client
from django.contrib.auth.models import User
from webapp.account.models import Account
from webapp.alerts.models import Alert, LamsonState
from webapp.blurb.models import Blurb
import os
import app.model.alerts as alerts

relay = relay(port=8823)
client = RouterConversation("somedude@localhost", "alerts_tests")
sender = "test@localhost"


badmsg = MailRequest('fakepeer', sender, "alerts-2@lookoutthere.com", open(home("tests/data/emails/confirmation.msg")).read())
badmsg['to'] = "alerts-2@lookoutthere.com"

#send the alerts urls to localhost
alerts.GOOGLE_URL = "localhost:8000"

def setup_func():
    user = User.objects.all()[0]
    account = Account(email="test@test.com",
                   user=user)
    account.save()
    client = Client(name="Beth",
                    user=account)
    client.save()

    LamsonState.objects.all().delete()
    q = queue.Queue(email('run/error'))
    q.clear()
    q = queue.Queue(email('run/alerts'))
    q.clear()



def teardown_func():
    Blurb.objects.all().delete()
    Alert.objects.all().delete()
    Account.objects.all().delete()
    Client.objects.all().delete()

@with_setup(setup_func, teardown_func)
def test_good_confirmation(msg=None):

    """
    This message should move the state into
    ALERTING.
    """
    alert = create_alert()
    
    addr = "alerts-%s@lookoutthere.com" % alert.id
    if not msg:
        msg = MailRequest('fakepeer', sender, addr, open(home("tests/data/emails/alert-confirmation.msg")).read())
    msg['to'] = addr
    Router.deliver(msg)
    q = queue.Queue(email('run/alerts'))
    assert q.count() == 0
    assert_in_state('app.handlers.alerts', msg['to'], sender, 'ALERTING') 


@with_setup(setup_func, teardown_func)
def test_bad_confirmation():
    Router.deliver(badmsg)
    q = queue.Queue(email('run/error'))
    assert q.count() == 2 #one for the alertsq module and one for alerts
    assert_in_state('app.handlers.alerts', badmsg['to'], sender, 'CONFIRMING')


@with_setup(setup_func, teardown_func)
def test_confirm_then_alert():
    """
    An alert sent after an account is confirmed should go right into
    ALERTING and alert objects should be created in the database.
    """
    alert = create_alert()

    addr = "alerts-%s@lookoutthere.com" % alert.id

    confirm = MailRequest('fakepeer', sender, addr, open(home("tests/data/emails/tim-confirmation.msg")).read())
    confirm['to'] = addr
    test_good_confirmation(msg=confirm)


    alertsmsg = MailRequest('fakepeer', "different@sender", addr, open(home("tests/data/emails/tim-alerts.msg")).read())
    alertsmsg['to'] = addr
    Router.deliver(alertsmsg)

    # there are 10 alerts in this alert email. since this is the test environment it will be dumped
    # into the alerts queue automatically, which will create the 10 alerts. Then it should be processed
    # by the alerts handler module, dumped into the queue again, thereby upping the alerts queue by one.
    assert len(Blurb.objects.all()) == 10, "There are %s blurbs." % len(Blurb.objects.all())
    q = queue.Queue(email('run/alerts'))
    assert q.count() == 1

    
    


@with_setup(setup_func, teardown_func)
def test_incoming_alert():
    """
    Verify an incoming alert generates
    the correct database records.
    """
    alert = create_alert()

    
    msg = MailRequest('fakepeer', sender, "alerts-%s@lookoutthere.com" % alert.id, open(home("tests/data/emails/beth-alerts.msg")).read())
    msg['to'] = "alerts-%s@lookoutthere.com" % alert.id
    Router.deliver(msg)

    #Should error out in the alerts.py handlers module in CONFIRMING
    #because these messages are dumped in the alertsq to be handled asyncronously,
    #but the testing environment just sends it to both modules at the same time.
    q = queue.Queue(email('run/error'))
    assert q.count() == 1
    
    assert len(Blurb.objects.all()) == 15, "There are %s blurbs." % len(Blurb.objects.all())

    
    


