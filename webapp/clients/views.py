from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from webapp.clients.forms import CreateClientForm, DisableClientForm
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
def disable(request):
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

