# Generated by Django 5.1.5 on 2025-01-23 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_delete_sessionpack'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='cn_dni',
            field=models.CharField(default='DEFAULT_DNI', max_length=15, unique=True),
        ),
        migrations.AddField(
            model_name='session',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('finished', 'Terminada')], default='pending', max_length=10),
        ),
    ]
