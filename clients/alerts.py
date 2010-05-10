import httplib, urllib, urllib2
import re
from BeautifulSoup import BeautifulSoup

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
byline = re.compile("By ([a-zA-Z]+ [a-zA-Z]+) ")

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
    response = send_confirmation(url)
    assert response.status == 200
    assert confirmed(response.read())


def send_confirmation(url):
    """
    Geneartes a request to the given
    confirmation url.
    """
    conn = httplib.HTTPConnection(GOOGLE_URL)
    conn.request("GET", url)
    response = conn.getresponse()
    conn.close()
    return response


def get_conf_url(body):
    """
    Scrapes the confirmation url from
    the confirmation email.
    """
    url = verify.findall(body)[0]
    return url


def confirmed(html):
    """
    Takes the html generated by the confirmation request and
    tries to determine if it was successfully confirmed or not.
    """
    soup = BeautifulSoup(html)

    error = soup.find(text=re.compile("error"))
    normal = soup.find(text=re.compile("Verified"))

    if error:
        message = error.replace("\n", "")
    elif normal:
        message = normal.replace("\n", "")
    else:
        message = ""

    if message == "An error has occurred.":
        return False
    elif message == "Google Alert Verified":
        return True
    else:
        return False


def parse_alerts(msg, alert):
    """
    Takes an alert and parses it into
    lists of alert stub instances and
    persists them to the database.
    """
    return []


def get_raw_alerts(html):
    """
    Given some html returns very basic
    parsing of the alerts.
    """
    soup = BeautifulSoup(html)
    return []


def get_html_stubs(html):
    """
    Takes in the html from an alerts email
    and returns a list.
    """
    soup = BeautifulSoup(html)
    tables = soup.p.findNextSiblings('table')
    trs = []
    for table in tables:
        trs.extend(table.findAll('tr', recursive=False))
        
    return [tr.find('td', recursive=False) for tr in trs]


def get_raw_alert(stub):
    """
    Given a stub of html beautiful soup, return
    a dictionary representing the alert.
    """
    
    #the first font tag contains the text nodes we want.
    blurb = ''.join(stub.find('font', recursive=False).findAll(text=True, recursive=False)).replace("\n", "")
    title = ''.join(stub.find('a', recursive=False).findAll(text=True)).replace("\n", "")
    source = stub.find('font', recursive=False).font.find(text=True)

    #Google wraps up the direct link in a query string, which goes
    #to them first then redirects. This gets the big link then pulls
    # the actual link out of the query string.
    bigUrl = stub.find('a', recursive=False)['href']
    url = urllib2.unquote(urllib2.urlparse.parse_qs(bigUrl)['q'][0])

    #get the byline
    by = ""
    mtch = byline.match(blurb)
    if mtch:
        by = mtch.groups()[0]
        
    return {'blurb' : blurb,
            'title' : title,
            'source' : source,
            'byline' : by,
            'url' : url}
    


