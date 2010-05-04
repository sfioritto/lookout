from nose.tools import *
from lamson.testing import *

relay = relay(port=8823)
client = RouterConversation("somedude@localhost", "alerts_tests")
sender = "test@localhost"
receiver = "google@localhost"
confmsg = MailRequest('fakepeer', sender, receiver, open("tests/data/emails/alert-confirmation.msg").read())

def test_incoming_confirmation():

    """
    """

    assert True


def test_incoming_alert():

    """
    """

    assert True



