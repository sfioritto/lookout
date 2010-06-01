from django.shortcuts import get_object_or_404
from webapp.clients.models import Client
from webapp.blurb.models import Blurb
from django.http import HttpResponseRedirect

def visit(request, clientid, blurbid):
    """
    Redirects someone who clicks on this link to the
    url of the blurb. Also marks the blurb as visited.
    """
    client = get_object_or_404(Client, pk=clientid)
    blurb = get_object_or_404(Blurb, pk=blurbid)
    if not blurb.visited:
        blurb.visited = True
        blurb.save()
    return HttpResponseRedirect(blurb.url)




