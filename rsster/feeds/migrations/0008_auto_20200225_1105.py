# Generated by Django 3.0.3 on 2020-02-25 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0007_auto_20200221_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='feeds',
            field=models.ManyToManyField(to='feeds.Feed'),
        ),
        migrations.DeleteModel(
            name='GroupFeed',
        ),
    ]
