from clients import alerts
from lamson.mail import MailRequest
import re

sender = "test@localhost"
receiver = "google@localhost"

msg = MailRequest('fakepeer', sender, receiver, open("tests/data/emails/alert-confirmation.msg").read())

def test_get_confirmation_url():

    """
    Scrape the confirmation url from the email.
    """
    
    body = msg.base.body
    url = alerts.get_conf_url(body)
    assert url == "/alerts/verify?gl=us&hl=en&s=AB2Xq4jYrbhsp8BlA12NFLDxGgFlmQQ2kF2WF5o"


