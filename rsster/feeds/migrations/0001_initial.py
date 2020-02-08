# Generated by Django 3.0.3 on 2020-02-07 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(db_index=True, max_length=255)),
                ('title', models.CharField(blank=True, default='', max_length=255)),
                ('image', models.CharField(blank=True, default='', max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('update_interval', models.IntegerField()),
                ('feed_last_publication', models.DateTimeField(auto_now_add=True)),
                ('web_url', models.CharField(blank=True, default='', max_length=255)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True, default='')),
                ('contents', models.TextField(blank=True, default='')),
                ('url', models.CharField(db_index=True, max_length=255)),
                ('guid', models.CharField(max_length=255)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('entry_created', models.DateTimeField(auto_now_add=True)),
                ('published', models.CharField(blank=True, db_index=True, default='', max_length=20)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feeds.Feed')),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
        ),
    ]
