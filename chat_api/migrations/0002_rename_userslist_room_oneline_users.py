# Generated by Django 5.0.2 on 2024-03-03 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='userslist',
            new_name='oneline_users',
        ),
    ]
