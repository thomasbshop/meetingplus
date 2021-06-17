from django.db import models

# Create your models here.
class Agenda(models.Model):
    item = models.TextField() 
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.item


class Minutes(models.Model):
    item = models.TextField() 

    def __str__(self):
        return self.item