from webapp.account.forms import CreateAccountForm
from django.template import RequestContext
from django.shortcuts import render_to_response

def create(request):
    
    form = CreateAccountForm()
    if request.method == "POST":
        form = CreateAccountForm(request.POST)
        
        #Check if the mailing list is valid.
        if form.is_valid():
            pass

    return render_to_response('account/create.html', {
            'form' : form,
            }, context_instance = RequestContext(request))



