from nose.tools import *
from lamson.testing import *
from lamson.routing import Router
from lamson.mail import MailRequest
from lamson import queue

relay = relay(port=8823)
client = RouterConversation("somedude@localhost", "alerts_tests")
sender = "test@localhost"
receiver = "alerts-1@lookoutthere.com"
confmsg = MailRequest('fakepeer', sender, receiver, open("tests/data/emails/alert-confirmation.msg").read())
confmsg['To'] = receiver


def setup_func():
    q = queue.Queue("run/error")
    q.clear()


def teardown_func():
    pass

@with_setup(setup_func, teardown_func)
def test_incoming_confirmation():

    """
    The confirmation link in the email is invalid,
    so it should fail. The handler shouuld handle
    this by logging a reason and dumping the message
    into the error queue. This test should also fail
    when running without an internet connection.
    """

    Router.deliver(confmsg)
    q = queue.Queue("run/error")
    assert q.count() == 1


def test_incoming_alert():

    """
    """

    assert True



