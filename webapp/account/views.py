

def create(request):
    
    form = AccountCreationForm()
    if request.method == "POST":
        form = CreateAccountForm(request.POST)
        
        #Check if the mailing list is valid.
        if form.is_valid():
            pass

    return render_to_response('account/create.html', {
            'form' : form,
            }, context_instance = RequestContext(request))



