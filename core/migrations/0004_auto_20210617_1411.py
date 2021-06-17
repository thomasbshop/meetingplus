# Generated by Django 3.2.4 on 2021-06-17 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210617_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='agenda',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.agendaitem'),
        ),
        migrations.AlterField(
            model_name='minute',
            name='minutes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.minuteitem'),
        ),
    ]