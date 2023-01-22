# Generated by Django 4.1.4 on 2023-01-12 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tname', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.user')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sname', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.user')),
            ],
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animalType', models.CharField(choices=[('F', 'Fish'), ('T', 'Turtle'), ('O', 'Octopus'), ('L', 'Lobster'), ('S', 'Shrimp')], max_length=1)),
                ('aname', models.CharField(max_length=20)),
                ('tank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.tank')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.user')),
            ],
        ),
    ]
