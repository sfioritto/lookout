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


#send the alerts urls to localhost
alerts.GOOGLE_URL = "localhost:8000"

def setup_func():
    user = User.objects.all()[0]
    account = Account(user=user)
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
def test_remove_url():

    """
    This message should update the remove url of the alert.
    """
    alert = create_alert()
    addr = "alerts-%s@lookoutthere.com" % alert.id
    #get into an 'ALERTING' state
    msg = MailRequest('fakepeer', sender, addr, open(home("tests/data/emails/confirmation.msg")).read())
    msg['to'] = addr
    Router.deliver(msg)
    q = queue.Queue(email('run/alerts'))
    assert q.count() == 0

    #send a regular alerts email
    msg = MailRequest('fakepeer', sender, addr, open(home("tests/data/emails/alerts.msg")).read())
    msg['to'] = addr
    Router.deliver(msg)
    assert len(Blurb.objects.all()) == 26, "There are %s blurbs, expected 15." % len(Blurb.objects.all())
    alert = Alert.objects.all()[0]
    assert alert.removeurl == u"/alerts/remove?s=AB2Xq4jsDy4ienBZYuYgWbzBWQ5i6LiD5L4y8JY&hl=en&gl=us&source=alertsmail&cd=4Ya67t6E3e4&cad=:s7:f1:v1:"


