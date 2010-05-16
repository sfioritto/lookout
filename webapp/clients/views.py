from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from webapp.clients.forms import CreateClientForm
from webapp.clients.models import Client


@login_required
def show(request):
    """
    Show all of the clients for a user.
    """
    account = request.user.get_profile()
    clients = account.client_set.all()
    return render_to_response('clients/show.html', {
            'clients' : clients
            }, context_instance = RequestContext(request))


@login_required
def create(request):
    """
    Create a new client.
    """
    account = request.user.get_profile()
    created = False

    form = CreateClientForm()
    if request.method == "POST":
        form = CreateClientForm(request.POST)
        name = form.data['name']
        client = Client(user=account,
                        name=name)
        client.save()
        return HttpResponseRedirect(reverse('webapp.clients.views.show'))

    return render_to_response('clients/create.html', {
            'form' : form,
            }, context_instance=RequestContext(request))
    

