from webapp.account.forms import CreateAccountForm, UpdateUserForm
from webapp.account.models import Account
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import login, authenticate, forms
from django.contrib.auth.models import User


#Django hack to let us put emails in the username field in the login form
forms.AuthenticationForm.base_fields['username'].max_length = 75 

@login_required
def profile(request):
    account = request.user.get_profile()
    return render_to_response('account/profile.html', {
            'account' : account,
            }, context_instance = RequestContext(request))


@login_required
def edit_profile(request):
    
    user = request.user
    account = user.get_profile()

    if request.method == "POST":
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.email = data['email']
            user.first_name = data['firstname']
            user.last_name = data['lastname']
            user.save()
            return HttpResponseRedirect(reverse(profile))
            
    elif request.method == "GET":
        form = UpdateUserForm({'username' : user.username,
                               'firstname' : user.first_name,
                               'lastname' : user.last_name,
                               'email' : user.email})

    else:
        raise Http404

    return render_to_response('account/edit-profile.html', {
            'account' : account,
            'form' : form,
            }, context_instance = RequestContext(request))


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



