# Generated by Django 4.2.16 on 2025-03-12 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_alter_course_coursecover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='open',
            field=models.BooleanField(default=False),
        ),
    ]
