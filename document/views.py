from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def document(request):
    try:
        # retrieve meeting with given id joined by the current user
        # meeting = request.user.meetings_added.get(id=meeting_id)
        # check if meeting has document
        document_id = 1
    except:
        # user is not invited to the meeting or meeting does not exist
        return HttpResponseForbidden("403: Not allowed here.")
    
    return render(request, 'meeting/document.html', {'document_id': document_id})