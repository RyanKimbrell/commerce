# Generated by Django 3.0.8 on 2020-08-21 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200821_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bid_object',
        ),
        migrations.AddField(
            model_name='listing',
            name='bid_object',
            field=models.ManyToManyField(to='auctions.Bid'),
        ),
    ]
