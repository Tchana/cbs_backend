# Generated by Django 4.2.16 on 2025-07-04 09:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_alter_chatgroup_groupe_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatgroup',
            name='id',
        ),
        migrations.RemoveField(
            model_name='groupmessage',
            name='id',
        ),
        migrations.AddField(
            model_name='chatgroup',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='groupmessage',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
