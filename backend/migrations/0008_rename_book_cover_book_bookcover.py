# Generated by Django 4.2.16 on 2025-03-04 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_alter_book_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='book_cover',
            new_name='bookCover',
        ),
    ]
