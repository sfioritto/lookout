from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from webapp.clients.models import Client
from webapp.alerts.models import Alert
from webapp.alerts.forms import CreateAlertForm
from app.model import alerts

@login_required
def show(request, clientid):
    """
    Show all of the alerts for a client.
    """
    client = get_object_or_404(Client, pk=clientid)
    alerts = client.alert_set.all()
    return render_to_response('alerts/show.html', {
            'alerts' : alerts,
            'client' : client,
            }, context_instance = RequestContext(request))


@login_required
def create(request, clientid):
    """
    Create a new alert for the given client.
    """
    client = get_object_or_404(Client, pk=clientid)
    account = request.user.get_profile()
    error = False

    form = CreateAlertForm()
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
            alerts.create_alert(alert.term, alert.email)
            alert.save()
            return HttpResponseRedirect(reverse("webapp.alerts.views.show", kwargs={'clientid':client.id}))
        except:
            #TODO: dump something in the error logs
            error = True


    return render_to_response('alerts/create.html', {
            'form' : form,
            'client' : client,
            'error' : error,
            }, context_instance=RequestContext(request))
    
