# Generated by Django 3.2.4 on 2021-06-15 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0003_alter_documentchat_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentchatmessage',
            old_name='room',
            new_name='document',
        ),
    ]