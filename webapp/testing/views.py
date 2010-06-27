import app.model.alerts as alerts
from conf import home
from django.http import HttpResponse, Http404
from webapp.testing.models import Confirmation


def good_disable(request):
    return HttpResponse()

def bad_disable(request):
    raise Http404

def good_verify(request):
    """
    This very simply returns a 200 response. The
    markup is the google alerts confirmation markup.
    """
    return HttpResponse(open(home("tests/data/html/good-verify.html")).read())


def bad_verify(request):
    """
    This returns a 200OK response. The markup
    is the google alerts invalid alert confirmation
    markup.
    """
    return HttpResponse(open(home("tests/data/html/bad-verify.html")).read())

def create(request):
    """
    Returns a 200OK. Assumes the alert is created with the defaults.
    """
    post = request.POST
    assert post[alerts.TYPES_NAME] == alerts.TYPES['comprehensive']
    assert post[alerts.FREQUENCY_NAME] == alerts.FREQUENCY['instant']
    assert post[alerts.LENGTH_NAME] == '50'
    c = Confirmation()
    c.save()
    return HttpResponse("Alert created. Sending email now.")
