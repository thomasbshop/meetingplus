from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Agenda(models.Model):
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class AgendaItem(models.Model):
    item = models.TextField() 
    complete = models.BooleanField(default=False)
    agenda = models.ForeignKey(Agenda, on_delete=CASCADE, blank=True, null=True)

    def __str__(self):
        return self.item


class Minute(models.Model):
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

class MinuteItem(models.Model):
    item = models.TextField() 
    minute = models.ForeignKey(Minute, on_delete=CASCADE, blank=True, null=True)

    def __str__(self):
        return self.item