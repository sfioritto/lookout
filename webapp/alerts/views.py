

def create_alert(request):

    """
    """

    if request.method == "POST":
        form = RequestForm(request.POST)
        email = form.data['email']
        return HttpResponseRedirect(reverse("webapp.alerts.show_all"))
    else:
        return render_to_response('marketing/create-alert.html',
                                  context_instance=RequestContext(request))


def show_all(request):

    """
    """

    



