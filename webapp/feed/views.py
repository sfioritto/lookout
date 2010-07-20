from django.shortcuts import render_to_response, get_object_or_404
from webapp.clients.models import Client
from webapp.blurb.models import Blurb
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


@login_required
def older(request, clientid):
    """
    Shows all of the older blurbs for the given client,
    except the first 10 which are displayed in the show
    view.
    """

    client = get_object_or_404(Client, pk=clientid)
    filters = client.get_filters()
    selected, options = get_options(filters)

    return render_to_response('feed/show.html', {'older' : client.older_blurbs()[10:],
                                                 'client' : client,
                                                 'olderind' : True,
                                                 'options' : options,
                                                 'selectedtext' : selected.text
                                                 }, context_instance = RequestContext(request))

@login_required
def show(request, clientid):
    """
    Shows all the blurbs for the client.
    """
    client = get_object_or_404(Client, pk=clientid)
    filters = client.get_filters()
    selected, options = get_options(filters)

    return render_to_response('feed/show.html', {'todays' : client.todays_blurbs(),
                                                 'yesterdays' : client.yesterdays_blurbs(),
                                                 'older' : client.older_blurbs()[:10], #only the first 10
                                                 'client' : client,
                                                 'options' : options,
                                                 'selectedtext' : selected.text
                                                 }, context_instance = RequestContext(request))

@login_required
def show_ajax(request, clientid):
    
    client = get_object_or_404(Client, pk=clientid)

    # This view can optionally accept a query string which defines
    # key value pairs which are used to define what blurbs show up
    # by default for the client.
    client.update_preferences(dict(request.GET.items()))

    return render_to_response('feed/show-inner.html', {'todays' : client.todays_blurbs(),
                                                       'yesterdays' : client.yesterdays_blurbs(),
                                                       'older' : client.older_blurbs(),
                                                       'client' : client,
                                                       }, context_instance = RequestContext(request))


def get_options(filters):
    """
    Returns a list of option objects used in templates for determining
    what to display in the filter configuration.
    """

    all = Option("all", "3")
    irrelevant = Option("only irrelevant", "2")
    relevant = Option("only relevant", "1")

    if filters.has_key('relevant') and filters['relevant']:
        # only relevant blurbs
        relevant.selected = True
        selected = relevant
    elif filters.has_key('relevant') and not filters['relevant']:
        # only irrelevant
        irrelevant.selected = True
        selected = irrelevant
    else:
        # all blurbs
        all.selected = True
        selected = all

    return selected, [relevant, irrelevant, all]


class Option:

    def __init__(self, text, value, selected=False):
        self.text = text
        self.selected = selected
        self.value = value
