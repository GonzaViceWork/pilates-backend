# Generated by Django 5.1.5 on 2025-02-01 00:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0014_attendancelog_room_session_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancelog',
            name='room',
        ),
    ]
