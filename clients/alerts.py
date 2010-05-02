import httplib, urllib

GOOGLE_URL = "google.com"
ALERTS_URL = "/alerts/create?gl=us&hl=en"
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




def create_alert(term, email, type='comprehensive', frequency='instant', length=50):

    """
    """

    assert frequency in FREQUENCY.keys(), "Must be one of %s" % FREQUENCY.keys()
    assert type in TYPES.keys(), "Must be one of %s" % TYPTES.keys()
    assert length == 50 or length == 20, "Length must be 50 or 20."

    params = create_params(term, email, type, frequency, length)
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,application/json"}
    conn = httplib.HTTPConnection(GOOGLE_URL)
    conn.request("POST", ALERTS_URL, params, headers)
    response = conn.getresponse()
    print response.status
    conn.close()


def create_params(term, email, type, frequency, length):

    return {
        TERM_NAME : term, 
        EMAIL_NAME : email,
        TYPES_NAME : type, 
        FREQUENCY_NAME : frequency,
        LENGTH : length}



