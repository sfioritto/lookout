from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from webapp.folders.models import Folder

@login_required
def show(request, folderid):
    """
    Show all of the alerts for a folder.
    """
    folder = get_object_or_404(Folder, pk=folderid)
    alerts = folder.alert_set.all()
    return render_to_response('alerts/show.html', {
            'alerts' : alerts,
            'folder' : folder,
            }, context_instance = RequestContext(request))


# @login_required
# def create_alert(request):

#     """
#     """

#     if request.method == "POST":
#         form = RequestForm(request.POST)
#         email = form.data['email']
#         return HttpResponseRedirect(reverse("webapp.alerts.show_all"))
#     else:
#         return render_to_response('marketing/create-alert.html',
#                                   context_instance=RequestContext(request))
