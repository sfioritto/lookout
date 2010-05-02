import httplib, urllib
import re

GOOGLE_URL = "www.google.com"
ALERTS_URL = "/alerts/create?hl=en&gl=us"
TYPES_NAME = "t"
EMAIL_NAME = "e"
FREQUENCY_NAME = "f"
LENGTH_NAME = "l"
TERM_NAME = "q"

TYPES = {
    'comprehensive' : 7,
    'news' : 1,
    'web' : 2,
    'blogs' : 4,
    'groups' : 8,
    'video' : 9
}

FREQUENCY = {
    'instant' : 0,
    'day' : 1,
    'week' : 6
}

verify = re.compile("/alerts/verify.*\w")

def create_alert(term, email, type='comprehensive', frequency='instant', length=50):

    """
    Creates a google alert for the given term and
    email.
    """

    assert frequency in FREQUENCY.keys(), "Must be one of %s" % FREQUENCY.keys()
    assert type in TYPES.keys(), "Must be one of %s" % TYPES.keys()
    assert length == 50 or length == 20, "Length must be 50 or 20."

    params = create_params(term, email, type, frequency, length)
    headers = {'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
    conn = httplib.HTTPConnection(GOOGLE_URL)
    conn.request("POST", ALERTS_URL, params, headers)
    response = conn.getresponse()
    conn.close()


def create_params(term, email, type, frequency, length):

    """
    Creates a url encoded POST string to send to
    google alerts service.
    """

    return urllib.urlencode({
        TERM_NAME : term, 
        EMAIL_NAME : email,
        TYPES_NAME : type, 
        FREQUENCY_NAME : frequency,
        LENGTH_NAME : length})


def confirm_alert(msg):

    """
    Takes a lamson message object, finds the confirmation
    url and confirms the creation of the alert.
    """
    
    url = get_conf_url(msg.base.body)
    send_confirmation(url)


def send_confirmation(url):

    conn = httplib.HTTPConnection(GOOGLE_URL)
    conn.request("GET", url)
    conn.close()


def get_conf_url(body):

    url = verify.findall(body)[0]
    return url
