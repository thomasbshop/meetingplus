# Generated by Django 3.2.4 on 2021-06-15 00:52

from django.db import migrations, models
import document.models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_alter_documentchat_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentchat',
            name='file',
            field=models.FileField(upload_to=document.models.document_directory_path),
        ),
    ]
