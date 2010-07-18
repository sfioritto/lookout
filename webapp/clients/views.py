from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from webapp.clients.forms import CreateClientForm, DisableClientForm, UpdateClientForm
from webapp.clients.models import Client


@login_required
def show(request):
    """
    Show all of the clients for a user.
    """
    account = request.user.get_profile()
    return render_to_response('clients/show.html', {
            'clients' : account.active_clients()
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
        if form.is_valid():
            name = form.cleaned_data['name']
            print len(name)
            client = Client(user=account,
                            name=name)
            client.save()
            return HttpResponseRedirect(reverse('webapp.clients.views.show'))

    return render_to_response('clients/create.html', {
            'form' : form,
            }, context_instance=RequestContext(request))


@login_required
def delete(request):
    """
    Disables a given client.
    """
    if request.method == "POST":
        form = DisableClientForm(request.POST)
        client = get_object_or_404(Client, pk=form.data['id'])
        client.disable()
        return HttpResponse()
    else:
        raise Http404


def update(request):
    """
    Updates a given client.
    """
    if request.method == "POST":
        form = UpdateClientForm(request.POST)
        client = get_object_or_404(Client, pk=form.data['id'])
        client.name = form.data['name']
        client.save()
        HttpResponse()
    else:
        raise Http404

