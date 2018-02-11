# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-11 15:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_confirmed', models.BooleanField(default=False)),
                ('steam_id', models.CharField(default=None, max_length=200, null=True)),
                ('location', models.CharField(default='India', max_length=200, null=True)),
                ('avatar', models.ImageField(blank=True, upload_to='profile_image')),
                ('status_CS', models.IntegerField(default=0, null=True)),
                ('status_FIFA', models.IntegerField(default=0, null=True)),
                ('is_subscribed', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=200)),
                ('tournament', models.CharField(default=None, max_length=200, null=True)),
                ('number_of_players', models.IntegerField(default=0)),
                ('game_on', models.IntegerField(default=0)),
                ('team_lock', models.IntegerField(default=0)),
                ('team_avatar', models.ImageField(blank=True, upload_to='team_image')),
                ('team_head', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal.Team')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament_name', models.CharField(default=None, max_length=200)),
                ('tournament_date', models.DateTimeField(default=None, null=True)),
                ('no_of_players', models.IntegerField(default=1, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='team_cs',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal.Team'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
