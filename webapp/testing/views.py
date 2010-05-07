from lookout.settings import home
from django.views.generic import simple
from django.http import HttpResponse

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
