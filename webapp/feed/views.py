from datetime import datetime as dt
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

    year = dt.today().year
    month = dt.today().month
    day = dt.today().day

    today = Blurb.objects.filter(client=client).filter(created_on__year=year,
                                                       created_on__month=month,
                                                       created_on__day=day).all()
    yesterday = Blurb.objects.filter(client=client).filter(created_on__year=year,
                                                       created_on__month=month,
                                                       created_on__day=day - 1).all()

    older = Blurb.objects.filter(client=client).filter(created_on__lt=dt(year, month, day-1)).all()

    return render_to_response('feed/show.html', {'today' : today,
                                                 'yesterday' : yesterday,
                                                 'older' : older,
                                                 'client' : client, 
                                                 }, context_instance = RequestContext(request))

