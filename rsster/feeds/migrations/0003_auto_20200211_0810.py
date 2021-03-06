# Generated by Django 3.0.3 on 2020-02-11 08:10

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_auto_20200207_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveFeeds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterModelManagers(
            name='entry',
            managers=[
                ('entries', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='feed',
            managers=[
                ('feeds', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='entry',
            name='guid',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
