# Generated by Django 3.0.8 on 2020-08-22 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20200822_2059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='comment_text',
        ),
    ]