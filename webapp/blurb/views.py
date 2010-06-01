from django.shortcuts import get_object_or_404
from webapp.clients.models import Client
from webapp.blurb.models import Blurb
from django.http import HttpResponseRedirect, HttpResponse, Http404

def visit(request, clientid, blurbid):
    """
    Redirects someone who clicks on this link to the
    url of the blurb. Also marks the blurb as visited.
    """
    blurb = get_object_or_404(Blurb, pk=blurbid)
    if not blurb.visited:
        blurb.visited = True
        blurb.save()
    return HttpResponseRedirect(blurb.url)


def relevance(request, clientid, blurbid):
    """
    Marks a blurb as irrelevant on a POST.
    """
    if request.method == "POST":
        blurb = get_object_or_404(Blurb, pk=blurbid)
        blurb.relevant = request.POST['relevance']
        blurb.save()
        return HttpResponse()
    else:
        raise Http404()




