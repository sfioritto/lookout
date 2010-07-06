from datetime import datetime as dt, timedelta as td
from django.shortcuts import render_to_response, get_object_or_404
from webapp.clients.models import Client
from webapp.blurb.models import Blurb
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def login_redirect(request, clientid):
    """
    Temporary, just for beta testers.
    """
    id = request.GET['id']
    if id == '3918862675d4db70b01d7e0c087c2a79d6fd855f':
        user = authenticate(username='christy', password='password')
    elif id = '98ba9c25be8d9ff043e4fdfd82c3f06af6f32f1c':
        user = authenticate(username='jackie', password='password')
    login(request, user)
    return HttpResponseRedirect(reverse(show, kwargs={'clientid':clientid}))

    else:
        raise Http404
        

@login_required
def older(request, clientid):
    """
    Shows all of the older blurbs for the given client,
    except the first 10 which are displayed in the show
    view.
    """

    client = get_object_or_404(Client, pk=clientid)

    yesterday = dt.today() - td(1)

    older = Blurb.objects.filter(client=client).filter(created_on__lt=dt(yesterday.year,
                                                                         yesterday.month,
                                                                         yesterday.day))\
                                                                         .filter(relevant=True)\
                                                                         .order_by('-created_on')\
                                                                         .all()[10:]
    return render_to_response('feed/show.html', {'older' : older,
                                                 'client' : client,
                                                 'olderind' : True,
                                                 }, context_instance = RequestContext(request))

@login_required
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
                                                                         .all()[:10]

    return render_to_response('feed/show.html', {'todays' : todays,
                                                 'yesterdays' : yesterdays,
                                                 'older' : older,
                                                 'client' : client, 
                                                 }, context_instance = RequestContext(request))

