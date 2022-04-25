from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import SortieForm, CommentForm, PhotoForm
from .models import Itineraire, Sortie, Commentaire


# Create your views here.

@login_required
def itineraires(request):
    """
    Prends les itinéraires créés et les affiches

    Args:
        request : la demande entrante
    """
    itineraires = get_list_or_404(Itineraire)
    return render(request, 'itineraires/itineraires.html', {'itineraires': itineraires})


@login_required
def sorties(request, itineraire_id):
    """
    Prends les sorties créés  et les affiches

    Args:
        request : la demande entrante
        itineraire_id : l'identifiant de l'itineraire 

    """
    sorties  = get_list_or_404(Sortie, itineraire_id = itineraire_id)
    itineraire = get_object_or_404(Itineraire, pk = itineraire_id)
    utilisateur = request.user
    return render(request, 'itineraires/sorties.html', {'sorties': sorties, 'itineraire': itineraire, 'utilisateur':utilisateur})


@login_required
def sortie(request, sortie_id):
    """
    Prend une sortie et affiche les détails

    Args:
        request : la demande entrante
        itineraire_id : l'identifiant de la sortie
    """
    sortie = get_object_or_404(Sortie, pk=sortie_id)    
    liste_commentaires = get_list_or_404(Commentaire, sortie = sortie_id)
    
    return render(request, 'itineraires/sorties_details.html', {'sortie': sortie, 'liste_commentaires' : liste_commentaires})


@login_required
def nouvelle_sortie(request, itineraire_id):
    """
    Crée une nouvelle sortie dans la base de donnée et pré-remplissage avec itinéraire
    Args:
        request: la demande entrante, GET or POST
        itineraire_id : l'identifiant de l'itinéraire auquel on ajoute une sortie
    Returns:
        - Une page avec un formulaire vide si c'est une requête GET,
        - Une page avec un formulaire pré-rempli si c'est une requête POST
          avec des mauvaises donnée,
        - ou une page avec la sortie ajouté
    """
    if request.method == 'GET':
        form = SortieForm()
    elif request.method == 'POST':
        form = SortieForm(request.POST)
        if form.is_valid():
            sortie = form.save(commit=False)
            sortie.utilisateur = request.user
            sortie.itineraire = get_object_or_404(Itineraire, pk=itineraire_id)#pré-rempli l'itinéraire
            sortie.save()
            return redirect('itineraires:sortie_details', sortie.id)
    itineraire = get_object_or_404(Itineraire, pk=itineraire_id )
    return render(request, 'itineraires/modif_sortie.html', {'form': form, 'itineraire': itineraire})


@login_required
def modif_sortie(request, sortie_id):
    """
    Modifie uen sortie déjà enregistée dans la base de donnée et pré-remplissage avec itinéraire
    Args:
        request: la demande entrante, GET or POST
        sortie_id : l'identifiant de la sortie à modifier
    Returns:
        - Une page avec un formulaire vide si c'est une requête GET,
        - Une page avec un formulaire pré-rempli si c'est une requête POST
          avec des mauvaises donnée,
        - ou une page avec la sortie modifié
    """
    sortie = get_object_or_404(Sortie, pk=sortie_id)
    if request.method == 'GET':
         form = SortieForm(instance=sortie)
    elif request.method == "POST":
        form = SortieForm(request.POST, instance=sortie)
        if form.is_valid():
            sortie = form.save(commit=False)
            sortie.utilisateur = request.user
            sortie.itineraire =  get_object_or_404(Itineraire, pk = sortie.itineraire.id) #pré-rempli l'itinéraire
            sortie.save()
            return redirect('itineraires:sortie_details', sortie_id)
    return render(request, 'itineraires/modif_sortie.html', {'form': form, 'itineraire' : sortie.itineraire, 'sortie' : sortie})


def ajout_commentaire(request, sortie_id):
    
    sortie = get_object_or_404(Sortie, pk=sortie_id)
    
    if request.method == 'POST':

        form = CommentForm(request.POST)
        if form.is_valid():

            commentaire = form.save(commit=False)
            commentaire.utilisateur_auteur = request.user
            commentaire.sortie = sortie
            commentaire.save()
            
            return redirect('itineraires:sortie_details', sortie_id)
    else:
      form = CommentForm()

    return render(request, 'itineraires/commentaire.html', {'form': form})

def photo_upload(request, sortie_id):
    
     sortie = get_object_or_404(Sortie, pk=sortie_id)
     form = PhotoForm()
     if request.method == 'POST':
         form = PhotoForm(request.POST, request.FILES)
         if form.is_valid():
             photo = form.save(commit = False)
             photo.uploader = request.user
             photo.sortie = sortie
             photo.save()
             return redirect('itineraires:sortie_details', sortie_id)
     else:
       form = PhotoForm()
        
     return render(request, 'itineraires/photo_upload.html', {'form' : form})

# def affichage_photo(request):
#     photos = models.Photo.objects.all()
#     return render(request, 'itineraires/sorties_details.html', context={'photos': photos})


