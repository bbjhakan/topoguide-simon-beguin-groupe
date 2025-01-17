# Generated by Django 4.0.4 on 2022-04-25 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itineraires', '0002_alter_itineraire_altitude_depart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='itineraire',
            name='latitude_arrivee',
            field=models.FloatField(default=1, verbose_name='Latitude point arrivée'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itineraire',
            name='latitude_depart',
            field=models.FloatField(default=1, verbose_name='Latitude point de départ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itineraire',
            name='longitude_arrivee',
            field=models.FloatField(default=1, verbose_name='Longitude point arrivée'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itineraire',
            name='longitude_depart',
            field=models.FloatField(default=1, verbose_name='Longitude point de départ'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sortie',
            name='date_sortie',
            field=models.CharField(max_length=20, verbose_name='Date de la sortie'),
        ),
        migrations.AlterField(
            model_name='sortie',
            name='difficulte_ressentie',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1, verbose_name='Difficulté ressentie (de 1 à 5)'),
        ),
        migrations.AlterField(
            model_name='sortie',
            name='experience',
            field=models.CharField(choices=[('Tous débutants', 'Tous débutants'), ('Tous expérimentés', 'Tous expérimentés'), ('Mixte', 'Mixte')], max_length=20, verbose_name='Expérience du groupe'),
        ),
        migrations.AlterField(
            model_name='sortie',
            name='meteo',
            field=models.CharField(choices=[('Bonne', 'Bonne'), ('Moyenne', 'Moyenne'), ('Mauvaise', 'Mauvaise')], max_length=20, verbose_name='Météo'),
        ),
    ]
