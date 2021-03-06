from django.db import models
from django.contrib.auth.models import User
from document.models import DocumentChat
from core.models import Agenda, Minute

class MeetingChatRoom(models.Model):
	# Room title
	title 		= models.CharField(max_length=255, unique=True, blank=False,)
	agenda		= models.OneToOneField(Agenda, on_delete=models.CASCADE, blank=True, null=True)
	minutes		= models.OneToOneField(Minute, on_delete=models.CASCADE, blank=True, null=True)
	# documents in this meeting
	documents   = models.ManyToManyField(
		DocumentChat,
		blank=True,
		related_name='meetings_added',
		help_text='Documents uploaded in this meeting.')
	# all users who are authenticated and viewing the chat
	users 		= models.ManyToManyField(
        User, 
        blank=True,
        related_name='meetings_added',
        help_text="users who are connected to meeting room.")

	def __str__(self):
		return self.title

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
		return "MeetingChatRoom-%s" % self.id


class MeetingRoomChatMessageManager(models.Manager):
    def by_room(self, room):
        qs = MeetingRoomChatMessage.objects.filter(room=room).order_by("-timestamp")
        return qs

class MeetingRoomChatMessage(models.Model):
    """
    Chat message created by a user inside a MeetingChatRoom
    """
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    room                = models.ForeignKey(MeetingChatRoom, on_delete=models.CASCADE)
    timestamp           = models.DateTimeField(auto_now_add=True)
    content             = models.TextField(unique=False, blank=False,)

    objects = MeetingRoomChatMessageManager()

    def __str__(self):
        return self.content