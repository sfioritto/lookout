from webapp.account.forms import CreateAccountForm
from webapp.account.models import Account
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import login, authenticate, forms
from django.contrib.auth.models import User


#Django hack to let us put emails in the username field in the login form
forms.AuthenticationForm.base_fields['username'].max_length = 75 


def create(request):
    """
    Create a django user object and a Lookout
    account object.
    """
    form = CreateAccountForm()
    if request.method == "POST":
        form = CreateAccountForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(data['username'], '', data['password'])
            user.save()
            account = Account(email=data['email'],
                              user=user)
            account.save()

            user = authenticate(username=user.username, password=data['password'])
            login(request, user)

            return HttpResponseRedirect("/")


    return render_to_response('account/create.html', {
            'form' : form,
            }, context_instance = RequestContext(request))



