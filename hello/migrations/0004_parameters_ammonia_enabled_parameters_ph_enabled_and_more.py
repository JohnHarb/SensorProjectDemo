# Generated by Django 4.1.7 on 2023-04-21 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_logdata_is_manual_profile_email_notifications_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='ammonia_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='parameters',
            name='ph_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='parameters',
            name='salinity_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='parameters',
            name='temp_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tank',
            name='parameters',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tank_for_parameters', to='hello.parameters'),
        ),
        migrations.AlterField(
            model_name='parameters',
            name='tank',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parameters_for_tank', to='hello.tank'),
        ),
    ]
