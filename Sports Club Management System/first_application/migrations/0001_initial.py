# Generated by Django 3.2.12 on 2022-04-24 14:04

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.IntegerField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=30)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('coach_id', models.IntegerField(primary_key=True, serialize=False)),
                ('biography', models.CharField(default='Bio', max_length=200)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.IntegerField(primary_key=True, serialize=False)),
                ('team_1_name', models.CharField(max_length=30)),
                ('team_2_name', models.CharField(max_length=30)),
                ('score', models.IntegerField()),
                ('Date', models.DateField(default=datetime.datetime.now)),
                ('Time', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Reserved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateTimeField(default=datetime.datetime.now)),
                ('Starting_hour', models.TimeField()),
                ('Ending_hour', models.TimeField()),
                ('Reserved', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('date_of_birth', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_name', models.CharField(max_length=30)),
                ('team_id', models.IntegerField(primary_key=True, serialize=False)),
                ('team_description', models.TextField(default='some description')),
                ('number_of_players', models.IntegerField()),
                ('max_number_of_players', models.IntegerField(default=30)),
                ('sports_type', models.CharField(max_length=30)),
                ('age_cat', models.IntegerField(default=1)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_application.coach')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.IntegerField(primary_key=True, serialize=False)),
                ('team_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_application.team')),
                ('user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_application.user')),
            ],
        ),
        migrations.CreateModel(
            name='Field_Reservation',
            fields=[
                ('reservation_id', models.IntegerField(primary_key=True, serialize=False)),
                ('Date', models.DateTimeField(default=datetime.datetime.now)),
                ('Starting_hour', models.CharField(max_length=30)),
                ('Ending_hour', models.CharField(max_length=30)),
                ('with_equip', models.BooleanField()),
                ('field_type', models.CharField(max_length=30)),
                ('court_number', models.IntegerField()),
                ('user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_application.user')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.IntegerField(primary_key=True, serialize=False)),
                ('with_food', models.BooleanField()),
                ('Date', models.DateTimeField(default=datetime.datetime.now)),
                ('Starting_hour', models.CharField(max_length=30)),
                ('Ending_hour', models.CharField(max_length=30)),
                ('user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_application.user')),
            ],
        ),
    ]
