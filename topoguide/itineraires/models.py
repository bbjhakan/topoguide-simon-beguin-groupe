from django.db import models
from django.db.models import IntegerField, Model
from django.contrib.auth.models import User

# Create your models here.

class Itineraire(models.Model):
    """
    Un itinéraire constitué du titre, du point de départ, de la latitude et longitude des points de départ et d'arrivée, de la description, de l'altitude de départ, 
    de l'altitude min, de l'altitude max, du dénivelé positif cumulé
    du dénivelé négatif cumulé dela durée estimée (en heures) de la difficulté estimée (de 1 à 5)
    """
    titre = models.CharField(max_length=200)
    point_depart = models.CharField('Point de départ',max_length=200)
    latitude_depart = models.FloatField('Latitude point de départ')
    longitude_depart = models.FloatField('Longitude point de départ')
    latitude_arrivee = models.FloatField('Latitude point arrivée')
    longitude_arrivee = models.FloatField('Longitude point arrivée')
    description = models.CharField(max_length=400)
    altitude_depart = models.FloatField('Altitude de départ (m)')
    altitude_minimale = models.FloatField('Altitude minimale (m)')
    altitude_maximale = models.FloatField('Altitude maximale (m)')
    denivele_positif_cumule = models.FloatField('Dénivelé positif cumulé (m)')
    denivele_negatif_cumule = models.FloatField('Dénivelé négatif cumulé (m)')
    duree = models.FloatField('Durée (en heure)')
    CHOIX_DIF = ((1,'1'),(2,'2'),(3,'3'), (4,'4'), (5,'5')) # Liste d'entier avec choix pour difficulté
    difficulte = models.IntegerField('Difficulté (de 1 à 5)', default=1,choices=CHOIX_DIF)

    
    def __str__(self):
        return self.titre
    
    
class Sortie(models.Model):
    """
    Une sortie constitué de l'utilisateur qui a enregistré la sortie, de l'itinéraire correspondant dans le topoguide, de la date de la sortie
    de la durée réelle (en heures), du nombre de personnes ayant participé à la sortie, de l'expérience du groupe (à choisir dans une liste tous débutants, tous expérimentés, mixte)
    de la météo (à choisir dans une liste bonne, moyenne, mauvaise) et de la difficulté ressentie (de 1 à 5)
    """
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE) #Référence à enregistrements d'autres tables avec le type ForeignKey
    itineraire = models.ForeignKey(Itineraire, on_delete=models.CASCADE)
    date_sortie = models.CharField('Date de la sortie', max_length= 20)
    duree_reelle = models.FloatField('Durée réelle (en heure)')
    CHOIX_EXP = (('Tous débutants','Tous débutants'),('Tous expérimentés','Tous expérimentés'),('Mixte','Mixte')) # Liste de caractères avec choix pour expérience
    nombre_personne = models.FloatField('Nombre de personnes ayant réalisé la sortie')
    experience = models.CharField('Expérience du groupe', max_length= 20,choices=CHOIX_EXP)
    CHOIX_METEO = (('Bonne','Bonne'),('Moyenne','Moyenne'),('Mauvaise','Mauvaise'))
    meteo = models.CharField('Météo', max_length= 20,choices=CHOIX_METEO)
    CHOIX_DIF = ((1,'1'),(2,'2'),(3,'3'), (4,'4'), (5,'5'))
    difficulte_ressentie = models.IntegerField('Difficulté ressentie (de 1 à 5)', default=1,choices=CHOIX_DIF)

    
    def __str__(self):
        return '%s %s'% (self.utilisateur, self.date_sortie)
    
    