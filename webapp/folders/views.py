from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def show(request):
    """
    Show all of the folders for a user.
    """
    account = request.user.get_profile()
    folders = account.folder_set.all()
    return render_to_response('folders/show.html', {
            'folders' : folders
            }, context_instance = RequestContext(request))
