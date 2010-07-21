from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from webapp.clients.models import Client
from django.http import Http404

def is_owner(func):
    
    def wrapped(request, *args, **kwargs):

        assert kwargs.has_key('clientid'), "is_owner can only be called on URLs with a clientid."
        clientid = kwargs['clientid']
        client = get_object_or_404(Client, pk=clientid)
        
        if client.user == request.user.get_profile():
            return func(request, *args, **kwargs)
        else:
            raise Http404

    # Must be logged in before calling the wrapped function.
    return login_required(wrapped)
    
    
