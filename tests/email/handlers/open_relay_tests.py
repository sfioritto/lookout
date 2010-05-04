from nose.tools import *
from lamson.testing import *
import os
from lamson import server

relay = relay(port=8823)
client = RouterConversation("somedude@lookoutthere.com", "requests_tests")
confirm_format = "testing-confirm-[0-9]+@"
noreply_format = "testing-noreply@"


def test_drops_open_relay_messages():
    """
    But, make sure that mail NOT for test.com gets dropped silently.
    """
    client.begin()
    client.say("tester@badplace.notinterwebs", "Relay should not happen")
    assert queue().count() == 0, "You are configured currently to accept everything.  You should change config/settings.py router_defaults so host is your actual host name that will receive mail."

