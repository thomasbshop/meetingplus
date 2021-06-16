import json
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from meetingplus.settings import MEDIA_ROOT, MEDIA_URL
from .models import DocumentChat
from .consumers import get_document_messages

# Create your views here.
@login_required
def document(request, document_id=15):
    try:
        # retrieve meeting with given id joined by the current user
        document = DocumentChat.objects.get(pk=document_id)
        # check if meeting has document
        document_path = f'{MEDIA_URL}{document.file}'
    except:
        # user is not invited to the meeting or meeting does not exist
        return HttpResponseForbidden("403: Not allowed here.")
    
    return render(request, 'meeting/document.html', 
    {'document_id': document_id, 'document_path': document_path})

async def document_messages(request, document_id):
    try:
        payload = await get_document_messages(document_id, page_number=1)
        if payload != None:
            payload = json.loads(payload)
            print("it is me", payload)
            return JsonResponse(payload)
    except:
        return HttpResponse(status=204)