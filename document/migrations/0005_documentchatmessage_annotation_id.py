# Generated by Django 3.2.4 on 2021-06-16 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0004_rename_room_documentchatmessage_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentchatmessage',
            name='annotation_id',
            field=models.TextField(default='annot_id'),
            preserve_default=False,
        ),
    ]