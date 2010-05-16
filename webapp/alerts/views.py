from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from webapp.clients.models import Client

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
def create_alert(request, clientid):
    """
    Create a new alert for the given client.
    """

    if request.method == "POST":
        form = RequestForm(request.POST)
        email = form.data['email']
        return HttpResponseRedirect(reverse("webapp.alerts.show_all"))
    else:
        return render_to_response('marketing/create-alert.html',
                                  context_instance=RequestContext(request))
