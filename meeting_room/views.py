from os import name
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from document.forms import DocumentChatForm

@login_required
def meeting_chat_room(request, meeting_id):
    # try:
    #     # retrieve meeting with given id joined by the current user
    #     meeting = request.user.meetings_added.get(id=meeting_id)
    # except:
    #     # user is not invited to the meeting or meeting does not exist
    #     return HttpResponseForbidden(f"403: Not allowed here.")
    
    return render(request, 'meeting/chat_room.html', {'meeting_id': meeting_id})

def room(request, room_name):
    return render(request, 'meeting/chat.html', {
        'room_name': room_name
    })

def upload_file(request):
    print(request.method)
    if request.method == "POST":
        form = DocumentChatForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            # return print('saved')
            return HttpResponse( "uploaded", content_type="application/json")
        else:
            print('not saved')
            return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),
                                content_type="application/json" )
    else:
        print("no success")
        form=DocumentChatForm()
    return render(request, "meeting/upload_document.html", {'form': form})


        # print(form_data)
        # # if the post request has a file under the input name 'theDocument', then save the file.
        # request_file = request.FILES['theDocument'] if 'theDocument' in request.FILES else None
        # if request_file and form_data:
        #     document = DocumentChat(name=form_data.documentName, file=request_file)
        #     document.save()
        #     # save attatched file
        #     # # create a new instance of FileSystemStorage
        #     # fs = FileSystemStorage()
        #     # file = fs.save(request_file.name, request_file)
        #     # the fileurl variable now contains the url to the file. This can be used to serve 
        #     # the file when needed.
        #     # fileurl = fs.url(file)
        #     # if file and form_data:
        #     #     document = DocumentChat(name=form_data.documentName, fileurl=fileurl)
        #     #     document.save()
        #     return HttpResponse( "uploaded", content_type="application/json")
        # else:
        #     return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),
        #                         content_type="application/json" )