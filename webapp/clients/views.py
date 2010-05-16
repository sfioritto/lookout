from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


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
