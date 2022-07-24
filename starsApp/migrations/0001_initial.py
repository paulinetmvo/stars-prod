# Generated by Django 4.0.4 on 2022-07-15 15:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import os

from django.contrib.auth.models import User
from django.db import migrations
from django.db.backends.postgresql.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps

import google.auth
from google.cloud import secretmanager


def createsuperuser(apps: StateApps, schema_editor: DatabaseSchemaEditor) -> None:
    """
    Dynamically create an admin user as part of a migration
    Password is pulled from Secret Manger (previously created as part of tutorial)
    """
    client = secretmanager.SecretManagerServiceClient()

    # Get project value for identifying current context
    _, project = google.auth.default()

    # Retrieve the previously stored admin password
    PASSWORD_NAME = os.environ.get("PASSWORD_NAME", "superuser-password")
    name = f"projects/{project}/secrets/{PASSWORD_NAME}/versions/latest"
    admin_password = client.access_secret_version(name=name).payload.data.decode(
        "UTF-8"
    )

    # Create a new user using acquired password, stripping any accidentally stored newline characters
    User.objects.create_superuser("admin", password=admin_password.strip())



class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(createsuperuser
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nummer', models.CharField(max_length=15, verbose_name='Nummer')),
            ],
        ),
        migrations.CreateModel(
            name='RoomDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bezeichnung', models.CharField(max_length=160, verbose_name='Bezeichnung')),
                ('anzahl', models.PositiveIntegerField(default=1, verbose_name='Anzahl')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('straße', models.CharField(default='Straße des 17. Juni', max_length=50, verbose_name='Straße')),
                ('hausnummer', models.CharField(default='135', max_length=10, verbose_name='Hausnummer')),
                ('postleitzahl', models.CharField(default='10623', max_length=5, verbose_name='Postleitzahl')),
                ('etage', models.IntegerField(default=0, verbose_name='Etage')),
            ],
        ),
        migrations.CreateModel(
            name='WorkplaceDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bezeichnung', models.CharField(max_length=160, verbose_name='Bezeichnung')),
                ('anzahl', models.PositiveIntegerField(default=1, verbose_name='Anzahl')),
            ],
        ),
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nummer', models.PositiveIntegerField()),
                ('anzahlPersonen', models.PositiveIntegerField(default=1)),
                ('sonstiges', models.CharField(blank=True, max_length=160, null=True)),
                ('barrierefrei', models.BooleanField(blank=True, default=True, null=True, verbose_name='Barrierefrei')),
                ('geraete', models.ManyToManyField(blank=True, to='starsApp.workplacedevice')),
                ('raum', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='starsApp.room')),
            ],
            options={
                'ordering': ['nummer'],
            },
        ),
        migrations.AddField(
            model_name='room',
            name='geraete',
            field=models.ManyToManyField(to='starsApp.roomdevice'),
        ),
        migrations.AddField(
            model_name='room',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='starsApp.unit'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(blank=True, max_length=3000)),
                ('rate', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('wp', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='starsApp.workplace')),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(14)])),
                ('sonstiges', models.CharField(max_length=160, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wp', models.ManyToManyField(to='starsApp.workplace')),
            ],
            options={
                'ordering': ['user'],
            },
        ),
    ]
