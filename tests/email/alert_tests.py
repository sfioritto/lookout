from lamson.mail import MailRequest
import re

sender = "test@localhost"
receiver = "google@localhost"

msg = MailRequest('fakeperr', sender, receiver, open("tests/data/emails/alert-confirmation.msg").read())

def test_get_confirmation_url():

    """
    Scrape the confirmation url from the email.
    """
    
    assert True


