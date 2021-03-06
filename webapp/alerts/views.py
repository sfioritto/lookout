from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from webapp.clients.models import Client
from webapp.alerts.models import Alert
from webapp.auth import is_owner
from webapp.alerts.forms import CreateAlertForm, DisableAlertForm
from app.model import alerts


@is_owner
def alert_list(request, clientid):
    """
    Return html for the list of alerts for ajax requests.
    """
    client = get_object_or_404(Client, pk=clientid)
    return render_to_response('alerts/list.html', {
            'alerts' : client.all_alerts(),
            'client' : client,
            })

@is_owner
def manage(request, clientid):
    """
    Show all of the alerts for a client.
    """

    client = get_object_or_404(Client, pk=clientid)
    return render_to_response('alerts/manage.html', {
            'alerts' : client.all_alerts(),
            'client' : client,
            'feed' : False,
            }, context_instance = RequestContext(request))



@is_owner
def disable(request, clientid):
    """
    Disable the given alert. A disabled alert can never be
    enabled.
    """
    if request.method == "POST":
        form = DisableAlertForm(request.POST)
        alert = get_object_or_404(Alert, pk=form.data['id'])
        alerts.disable_alert(alert.removeurl)
        alert.disabled = True
        alert.save()
        return HttpResponse()
    else:
        raise Http404


@is_owner
def create(request, clientid):
    """
    Create a new alert for the given client.
    """
    client = get_object_or_404(Client, pk=clientid)
    account = request.user.get_profile()

    if request.method == "POST":
        form = CreateAlertForm(request.POST)
        term = form.data['term']
        alert = Alert(user=account,
                      client=client,
                      term=term,
                      type='comprehensive',
                      frequency='instant',
                      length=50)
        try:
            alert.save()
            alerts.create_alert(alert.term, alert.email)
            return HttpResponse()
        except:
            #TODO: dump something in the error logs
            raise Http404
    else:
        raise Http404


    return render_to_response('alerts/create.html', {
            'form' : form,
            'client' : client,
            'error' : error,
            }, context_instance=RequestContext(request))
    
