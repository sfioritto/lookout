from django.shortcuts import render_to_response, get_object_or_404
from webapp.folders.models import Folder
from webapp.blurb.models import Blurb
from django.http import HttpResponse

def show(request, folderid):
    """
    Shows all the blurbs for the folder.
    """
    folder = get_object_or_404(Folder, pk=folderid)
    blurbs = Blurb.objects.filter(folder=folder).all()
    return render_to_response('feed/show.html', {'blurbs' : blurbs,
                                                 'folder' : folder})

