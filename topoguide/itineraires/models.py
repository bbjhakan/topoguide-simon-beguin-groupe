from django.db import models
from django.db.models import IntegerField, Model
from django.contrib.auth.models import User
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator


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
    description = models.CharField(max_length=2000)
    altitude_depart = models.PositiveIntegerField('Altitude de départ (m)')
    altitude_minimale = models.PositiveIntegerField('Altitude minimale (m)')
    altitude_maximale = models.PositiveIntegerField('Altitude maximale (m)')
    denivele_positif_cumule = models.PositiveIntegerField('Dénivelé positif cumulé (m)')
    denivele_negatif_cumule = models.PositiveIntegerField('Dénivelé négatif cumulé (m)')
    duree = models.PositiveIntegerField('Durée (en heure)',validators=[MinValueValidator(1)])
    CHOIX_DIF = ((1,'1'),(2,'2'),(3,'3'), (4,'4'), (5,'5')) # Liste d'entier avec choix pour difficulté
    difficulte = models.IntegerField('Difficulté (de 1 à 5)', default=1,choices=CHOIX_DIF)


    def __str__(self):
        return self.titre
    
    
class Sortie(models.Model):
    """
    Une sortie constituée de l'utilisateur qui a enregistré la sortie, de l'itinéraire correspondant dans le topoguide, de la date de la sortie
    de la durée réelle (en heures), du nombre de personnes ayant participé à la sortie, de l'expérience du groupe (à choisir dans une liste tous débutants, tous expérimentés, mixte)
    de la météo (à choisir dans une liste bonne, moyenne, mauvaise) et de la difficulté ressentie (de 1 à 5)
    """
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE) #Référence à enregistrements d'autres tables avec le type ForeignKey
    itineraire = models.ForeignKey(Itineraire, on_delete=models.CASCADE)
    date_sortie = models.DateField('Date de la sortie',validators=[MaxValueValidator(limit_value=datetime.date.today)])
    duree_reelle = models.IntegerField('Durée réelle (en heure)',validators=[MinValueValidator(1)])
    CHOIX_EXP = (('Tous débutants','Tous débutants'),('Tous expérimentés','Tous expérimentés'),('Mixte','Mixte')) # Liste de caractères avec choix pour expérience
    nombre_personne = models.PositiveIntegerField('Nombre de personnes ayant réalisé la sortie', validators=[MinValueValidator(1)])
    experience = models.CharField('Expérience du groupe', max_length= 20,choices=CHOIX_EXP)
    CHOIX_METEO = (('Bonne','Bonne'),('Moyenne','Moyenne'),('Mauvaise','Mauvaise'))
    meteo = models.CharField('Météo', max_length= 20,choices=CHOIX_METEO)
    CHOIX_DIF = ((1,'1'),(2,'2'),(3,'3'), (4,'4'), (5,'5'))
    difficulte_ressentie = models.IntegerField('Difficulté ressentie (de 1 à 5)', default=1,choices=CHOIX_DIF)
    photos = models.ImageField(upload_to='photos')
    
    def __str__(self):
        return '%s %s'% (self.utilisateur, self.date_sortie)
    
class Commentaire(models.Model):
    """
    Un commentaire est associé à une seule sortie et à un seul utilisateur. 
    On lui attribue automatiquement la date et l'heure à laquelle celui-ci est écrit.
    L'attribut texte enregistre le contenu du commentaire.
    L'attribut statut, qui rend visible le commentaire si sa valeur est True, et le cache sinon.
    """
    sortie = models.ForeignKey(Sortie, on_delete=models.CASCADE) 
    date = models.DateTimeField(default = datetime.datetime.now() )
    utilisateur_auteur = models.ForeignKey(User, on_delete=models.CASCADE) 
    texte = models.TextField()
    statut = models.BooleanField( default = True )

class Photo(models.Model):
    """
    Une photo est associée à une seule sortie et à un seul uploader.
    L'attribut image enregistre la photo.
    On lui attache aussi automatiquement la date à laquelle celle-ci est postée.
    """
    image = models.ImageField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    sortie = models.ForeignKey(Sortie, on_delete = models.CASCADE)
    date_created = models.DateTimeField(default = datetime.datetime.now())
    
    