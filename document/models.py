from django.db import models
from django.contrib.auth.models import User
from meeting_room.models import MeetingChatRoom

def get_profile_image_filepath(self, filename):
	return 'uploads/' + str(self.pk)

def get_default_profile_image():
	return "uploads/document.pdf"

def document_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/<filename>
    return 'uploads/{0}-{1}'.format(instance, filename)
	
class DocumentChat(models.Model):
	
	# Document title
	name 		= models.CharField(max_length=255, blank=False,)
	file        = models.FileField(upload_to=document_directory_path)

    # all users who are authenticated and viewing the chat ---room
    # users 		= models.ManyToManyField(
    #     User, 
    #     blank=True,
    #     related_name='meetings_added',
    #     help_text="users who are connected to meeting room.")
	
	def __str__(self):
		return f'{self.name}'

	def connect_user(self, user):
		"""
		return true if user is added to the users list
		"""
		is_user_added = False
		if not user in self.users.all():
			self.users.add(user)
			self.save()
			is_user_added = True
		elif user in self.users.all():
			is_user_added = True
		return is_user_added 


	def disconnect_user(self, user):
		"""
		return true if user is removed from the users list
		"""
		is_user_removed = False
		if user in self.users.all():
			self.users.remove(user)
			self.save()
			is_user_removed = True
		return is_user_removed 


	@property
	def group_name(self):
		"""
		Returns the Channels Group name that sockets should subscribe to to get sent
		messages as they are generated.
		"""
		return "DocumentChat-%s" % self.id
		
	
class DocumentChatMessageManager(models.Manager):
	def by_room(self, room):
		qs = DocumentChatMessage.objects.filter(room=room).order_by("-timestamp")
		return qs

class DocumentChatMessage(models.Model):
    """
    Chat message created by a user inside a DocumentChat
    """
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    room                = models.ForeignKey(DocumentChat, on_delete=models.CASCADE)
    timestamp           = models.DateTimeField(auto_now_add=True)
    content             = models.TextField(unique=False, blank=False,)

    objects = DocumentChatMessageManager()

    def __str__(self):
        return self.content