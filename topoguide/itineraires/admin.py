from unicodedata import name
from django.contrib import admin
from .models import Itineraire, Sortie,Commentaire, Photo


# Register your models here.
class ItineraireAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['titre']}),
        (None,               {'fields': ['point_depart']}),
        (None,               {'fields': ['description']}),
        (None,               {'fields': ['altitude_depart']}),
        (None,               {'fields': ['altitude_minimale']}),
        (None,               {'fields': ['altitude_maximale']}),
        (None,               {'fields': ['denivele_positif_cumule']}),
        (None,               {'fields': ['denivele_negatif_cumule']}),
        (None,               {'fields': ['duree']}),
        (None,               {'fields': ['difficulte']})
    ]
admin.site.register(Itineraire, ItineraireAdmin)

class SortieAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['utilisateur']}),
        (None,               {'fields': ['itineraire']}),
        (None,               {'fields': ['date_sortie']}),      
        (None,               {'fields': ['duree_reelle']}),
        (None,               {'fields': ['nombre_personne']}),
        (None,               {'fields': ['experience']}),
        (None,               {'fields': ['meteo']}),
        (None,               {'fields': ['difficulte_ressentie']}),
    ]
admin.site.register(Sortie, SortieAdmin)

class CommentaireAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['utilisateur_auteur']}),
        (None,               {'fields': ['date']}),
        (None,               {'fields': ['sortie']}),
        (None,               {'fields': ['texte']}),
    ]
admin.site.register(Commentaire, CommentaireAdmin)
admin.site.register(Photo)

