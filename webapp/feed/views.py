from datetime import datetime as dt, timedelta as td
from django.shortcuts import render_to_response, get_object_or_404
from webapp.clients.models import Client
from webapp.blurb.models import Blurb
from django.http import HttpResponse
from django.template import RequestContext

def show(request, clientid):
    """
    Shows all the blurbs for the client.
    """
    client = get_object_or_404(Client, pk=clientid)

    today = dt.today()
    yesterday = dt.today() - td(1)

    todays = Blurb.objects.filter(client=client).filter(created_on__year=today.year,
                                                        created_on__month=today.month,
                                                        created_on__day=today.day)\
                                                        .filter(relevant=True)\
                                                        .order_by('-created_on')\
                                                        .all()

    yesterdays = Blurb.objects.filter(client=client).filter(created_on__year=yesterday.year,
                                                       created_on__month=yesterday.month,
                                                       created_on__day=yesterday.day)\
                                                       .filter(relevant=True)\
                                                       .order_by('-created_on')\
                                                       .all()

    older = Blurb.objects.filter(client=client).filter(created_on__lt=dt(yesterday.year,
                                                                         yesterday.month,
                                                                         yesterday.day))\
                                                                         .filter(relevant=True)\
                                                                         .order_by('-created_on')\
                                                                         .all()

    return render_to_response('feed/show.html', {'todays' : todays,
                                                 'yesterdays' : yesterdays,
                                                 'older' : older,
                                                 'client' : client, 
                                                 }, context_instance = RequestContext(request))

