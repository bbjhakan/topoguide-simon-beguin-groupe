# Generated by Django 4.0.4 on 2022-04-25 13:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itineraires', '0004_sortie_photos_alter_commentaire_date_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 25, 15, 2, 7, 8940)),
        ),
    ]
