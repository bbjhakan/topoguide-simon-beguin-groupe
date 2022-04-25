from django import forms
from .models import Sortie, Commentaire, Photo
import datetime
class SortieForm(forms.ModelForm):
    """
    Simple formulaire, choix des items à afficher
    """
    
    edit_sortie = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = Sortie
        
        fields = ['date_sortie', 'duree_reelle', 'nombre_personne', 'experience', 'meteo', 'difficulte_ressentie']
        file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        

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
        
        #Commentaire.date = datetime.date.today
    
        fields = ['texte' ]
        
class PhotoForm(forms.ModelForm):
    edit_photo = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta : 
        model = Photo
        fields = ['image']
    