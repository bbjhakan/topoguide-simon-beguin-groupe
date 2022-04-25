from django import forms

from .models import Sortie, Commentaire

class SortieForm(forms.ModelForm):
    """
    Simple formulaire, choix des items à afficher
    """
    class Meta:
        model = Sortie
        fields = ['date_sortie', 'duree_reelle', 'nombre_personne', 'experience', 'meteo', 'difficulte_ressentie']
        
class CommentForm(forms.ModelForm):
    texte = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Commentez ici !',
        'rows':5,
        'cols':50
    }))
    class Meta:
        model = Commentaire
        fields = ['texte'] 