# Generated by Django 3.2.4 on 2021-06-17 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210617_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agenda',
            name='agenda',
        ),
        migrations.RemoveField(
            model_name='minute',
            name='minutes',
        ),
        migrations.AddField(
            model_name='agenda',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='agendaitem',
            name='agenda',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.agenda'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='minute',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='minuteitem',
            name='minute',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.minute'),
            preserve_default=False,
        ),
    ]
