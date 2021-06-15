# Generated by Django 3.2.4 on 2021-06-14 14:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meeting_room', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingchatroom',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='users who are connected to meeting room.', related_name='meetings_added', to=settings.AUTH_USER_MODEL),
        ),
    ]
