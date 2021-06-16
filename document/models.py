from django.db import models
from django.contrib.auth.models import User


def get_default_document():
	return "uploads/document.pdf"

def document_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/<filename>
    return 'uploads/{0}-{1}'.format(instance, filename)
	
class DocumentChat(models.Model):
	
	# Document title
	name 		= models.CharField(max_length=255, blank=False,)
	file        = models.FileField(upload_to=document_directory_path)

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
	def by_document(self, document):
		qs = DocumentChatMessage.objects.filter(document=document).order_by("-timestamp")
		return qs

class DocumentChatMessage(models.Model):
	"""
	Chat message created by a user inside a DocumentChat
	"""
	user                = models.ForeignKey(User, on_delete=models.CASCADE)
	document            = models.ForeignKey(DocumentChat, on_delete=models.CASCADE)
	timestamp           = models.DateTimeField(auto_now_add=True)
	annotationId		= models.TextField(verbose_name='annotationId', blank=False)
	content             = models.TextField(unique=False, blank=False,)
	
	objects = DocumentChatMessageManager()