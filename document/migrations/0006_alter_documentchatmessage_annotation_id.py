# Generated by Django 3.2.4 on 2021-06-16 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0005_documentchatmessage_annotation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentchatmessage',
            name='annotation_id',
            field=models.TextField(verbose_name='annotationId'),
        ),
    ]
