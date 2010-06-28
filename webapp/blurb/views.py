from django.shortcuts import get_object_or_404
from webapp.blurb.models import Blurb, IrrelevantBlurb
from webapp.clients.models import Client
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required

@login_required
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

@login_required
def relevance(request, clientid, blurbid):
    """
    Marks a blurb as irrelevant on a POST.
    """
    if request.method == "POST":

        blurb = get_object_or_404(Blurb, pk=blurbid)
        client = get_object_or_404(Client, pk=clientid)

        rel = False
        if request.POST['relevance'] == 'true':
            rel = True

        blurb.relevant = rel
        blurb.save()

        #add this blurb to the queue to be processed by the bayesian filter
        #process later.
        if not blurb.relevant:
            ib = IrrelevantBlurb(blurb=blurb,
                                 client=client)
            ib.save()
        # oops, didn't mean to mark that as irrelevant, remove from the queue
        else:
            IrrelevantBlurb.objects.filter(blurb=blurb).delete()

        return HttpResponse()
    else:
        raise Http404()




