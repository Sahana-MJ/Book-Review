# Generated by Django 4.1.1 on 2022-09-20 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(default=None, max_length=5000, null=True),
        ),
    ]
