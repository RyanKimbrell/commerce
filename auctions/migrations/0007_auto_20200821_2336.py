# Generated by Django 3.0.8 on 2020-08-21 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200821_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bid_object',
            field=models.ManyToManyField(blank=True, to='auctions.Bid'),
        ),
    ]
