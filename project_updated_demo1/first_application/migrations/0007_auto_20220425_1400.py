# Generated by Django 3.2.12 on 2022-04-25 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_application', '0006_alter_team_training_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='Ending_hour',
            field=models.TimeField(default='00:00:00'),
        ),
        migrations.AlterField(
            model_name='team',
            name='Starting_hour',
            field=models.TimeField(default='00:00:00'),
        ),
    ]
