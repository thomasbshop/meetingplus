from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


# @login_required
def meeting_chat_room(request, meeting_id):
    try:
        # retrieve meeting with given id joined by the current user
        meeting = request.user.meetings_added.get(id=meeting_id)
    except:
        # user is not invited to the meeting or meeting does not exist
        return HttpResponseForbidden("403: Not allowed here.")
    
    return render(request, 'meeting/chat_room.html', {'meeting_id': meeting_id})

def room(request, room_name):
    return render(request, 'meeting/chat.html', {
        'room_name': room_name
    })