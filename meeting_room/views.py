from django.http.response import HttpResponseRedirect
from document.models import DocumentChat
from os import name
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from meetingplus.settings import MEDIA_URL
from document.forms import DocumentChatForm
from core.models import AgendaItem, MinuteItem
from .models import MeetingChatRoom


@login_required()
def room(request, meeting_id=1):
    meeting_documents = MeetingChatRoom(pk=meeting_id).documents.all()
    if meeting_documents:
        # retrieve meeting with given id joined by the current user
        # check if meeting has document
        document_path = f'{MEDIA_URL}{meeting_documents[0].file}'
        context = {
            'meeting': meeting_id, 
            'document_id': meeting_documents[0].id,
            'document_path': document_path,
            'meeting_documents': meeting_documents
            }
        return render(request, 'meeting/document.html', context)
    context = {'meeting': meeting_id, 'meeting_documents': meeting_documents}
    return render(request, 'meeting/minutes.html', context)

@login_required
def meeting_chat_room(request, meeting_id=1):
    try:
        # retrieve meeting with given id joined by the current user
        meeting = MeetingChatRoom(id=meeting_id)
        meeting = MeetingChatRoom.objects.get(id=meeting_id)
        meeting_documents = meeting.documents.all()
    except:
        # user is not invited to the meeting or meeting does not exist
        return HttpResponseForbidden(f"403: Not allowed here.")
    return render(request, 'meeting/chat_room.html', {'meeting_id': meeting_id, 'meeting_documents': meeting_documents})

@login_required()
def agenda(request):
    meeting_id = 1
    meeting = MeetingChatRoom.objects.get(id=meeting_id)
    meeting_documents = meeting.documents.all()
    agenda = meeting.agenda
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        new_item = request.POST['item']
        item = AgendaItem(agenda=agenda, item=new_item)
        item.save()
        return HttpResponseRedirect(request.path_info)
    agenda_items = AgendaItem.objects.filter(agenda=agenda)
    context = {'agenda_items': agenda_items, 'meeting_documents': meeting_documents}
    return render(request, 'meeting/agenda.html', context)

@login_required()
def minutes(request):
    meeting_id = 1
    meeting = MeetingChatRoom.objects.get(id=meeting_id)
    meeting_documents = meeting.documents.all()
    agenda, minutes = meeting.agenda, meeting.minutes
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        new_item = request.POST['item']
        item = MinuteItem(minute=minutes, item=new_item)
        item.save()
        return HttpResponseRedirect(request.path_info)
    agenda_items = AgendaItem.objects.filter(agenda=agenda)
    minutes_items = MinuteItem.objects.filter(minute=minutes)
    context = {
        'agenda_items': agenda_items, 'minutes_items': minutes_items, 
        'meeting_documents': meeting_documents }
    return render(request, 'meeting/minutes.html', context)

def upload_file(request):
    if request.method == "POST":
        form = DocumentChatForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            instance = DocumentChat(name=name, file=request.FILES['file'])
            instance.save()
            # add to a meet
            meeting_id = form.cleaned_data.get('meeting_id', 1)
            room = MeetingChatRoom.objects.get(id=meeting_id)
            room.documents.add(instance)
            return HttpResponse( "uploaded", content_type="application/json")
        else:
            print('not saved')
            return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),
                                content_type="application/json" )
    else:
        print("no success")
        form=DocumentChatForm()
    return render(request, "meeting/upload_document.html", {'form': form})
