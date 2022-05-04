# Generated by Django 4.0.4 on 2022-05-04 14:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itineraires', '0012_alter_commentaire_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 4, 16, 47, 27, 286666)),
        ),
        migrations.AlterField(
            model_name='itineraire',
            name='latitude_arrivee',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=10, verbose_name='Latitude point arrivée (°)'),
        ),
        migrations.AlterField(
            model_name='itineraire',
            name='latitude_depart',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=10, verbose_name='Latitude point de départ (°)'),
        ),
        migrations.AlterField(
            model_name='itineraire',
            name='longitude_arrivee',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=10, verbose_name='Longitude point arrivée (°)'),
        ),
        migrations.AlterField(
            model_name='itineraire',
            name='longitude_depart',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=10, verbose_name='Longitude point de départ (°)'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 4, 16, 47, 27, 287072)),
        ),
    ]
