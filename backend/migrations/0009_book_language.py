# Generated by Django 4.2.16 on 2025-03-10 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_rename_book_cover_book_bookcover'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
