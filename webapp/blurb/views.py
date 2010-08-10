from django.shortcuts import get_object_or_404
from webapp.auth import is_owner
from webapp.blurb.models import Blurb
from webapp.clients.models import Client
from django.http import HttpResponseRedirect, HttpResponse, Http404

@is_owner
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


@is_owner
def reject(request, clientid, blurbid):
    """
    Marks a blurb as rejected on a POST.
    """
    if request.method == "POST":

        blurb = get_object_or_404(Blurb, pk=blurbid)
        blurb.reject()

        return HttpResponse()
    else:
        raise Http404()


@is_owner
def approve(request, clientid, blurbid):
    """
    Marks a blurb as approved on a POST.
    """
    if request.method == "POST":

        blurb = get_object_or_404(Blurb, pk=blurbid)
        blurb.approve()

        return HttpResponse()
    else:
        raise Http404()





