from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.utils import timezone
from .forms import SortieForm, CommentForm, PhotoForm
from .models import Itineraire, Sortie, Commentaire, Photo

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
    sortie_query = Sortie.objects.all()

    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    difficulte = request.GET.get('difficulte')
    duree_min = request.GET.get('duree_min')
    duree_max = request.GET.get('duree_max')
    itineraire = get_object_or_404(Itineraire, pk = itineraire_id)
    utilisateur = request.user
    
    if is_valid_query(date_min):
        sortie_query = sortie_query.filter(date_sortie__gte=date_min)                                       
    if is_valid_query(date_max):
        sortie_query = sortie_query.filter(date_sortie__lt=date_max)                                       
    
    if is_valid_query(difficulte):
        sortie_query = sortie_query.filter(difficulte_ressentie = difficulte)
    
    if is_valid_query(duree_min):
        sortie_query = sortie_query.filter(duree_reelle__gte=duree_min)                                       
    if is_valid_query(duree_max):
        sortie_query = sortie_query.filter(duree_reelle__lte=duree_max) 
    return render(request, 'itineraires/sorties.html', {'itineraire': itineraire, 'utilisateur':utilisateur, 'qs': sortie_query, 'date_min': date_min, 'date_max': date_max, 'difficulte': difficulte,'duree_min': duree_min, 'duree_max': duree_max})


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
    photos = get_list_or_404(Photo, sortie = sortie_id)
    
    return render(request, 'itineraires/sorties_details.html', {'sortie': sortie, 'liste_commentaires' : liste_commentaires, 'photos' : photos})


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
            sortie.itineraire = get_object_or_404(Itineraire, pk=itineraire_id) #pré-rempli l'itinéraire
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


def is_valid_query(param):
    """ Vérifie si le paramètre est valide

    Args:
        param : contenu de la barre de recherche/d'un filtre

    Returns:
        booléen : vrai s'il existe un champ dans la barre de recherche/le filtre
    """
    return param != '' and param is not None


def SearchView(request):
    """ 
    Permet d'afficher les itinéraires/sorties qui correspondent à la demande via la barre de recherche

    Args:
        request : la demande entrante

    Returns:
        - une page avec le résultat de la recherche
        Sur cette page, on peut appliquer un certain nombre de filtres pour filtrer les résultats de la recherche.
        S'il n'y a pas de résultat, on indique à l'utilisateur qu'il n'existe pas de résultats correspondant à sa recherche.
    """
    itineraire_query = Itineraire.objects.all()
    sortie_query = Sortie.objects.all()
    
    query = request.GET.get('barre_recherche') ##récupère le champ à l'intérieur de la barre de recherche

    difficulte = request.GET.get('difficulte') ##récupère le champ à l'intérieur du filtre correspondant à la difficulté souhaitée
    duree_min = request.GET.get('duree_min') ##récupère le champ à l'intérieur du filtre correspondant à la durée minimale souhaitée
    duree_max = request.GET.get('duree_max') ##récupère le champ à l'intérieur du filtre correspondant à la durée maximale souhaitée
    
    
    if is_valid_query(query):
        itineraire_query = itineraire_query.filter(Q(titre__icontains = query)  | ##on cherche dans le titre de l'itinéraire
                                                   Q(description__icontains = query) | ## ou dans la description de l'itinéraire
                                                   Q(point_depart__icontains = query)) ## ou dans le nom du point de départ
        sortie_query = sortie_query.filter(Q(utilisateur__username__icontains = query) | ##on cherche dans le nom d'utilisateur
                                           Q(itineraire__titre__icontains = query)).order_by('utilisateur') ##ou dans le titre de l'itinéraire auquel la sortie est associée
                                      
    
    if is_valid_query(difficulte):
        itineraire_query = itineraire_query.filter(difficulte = difficulte) ##on récupère uniquement les itinéraires avec la difficulté estimée précisée
        sortie_query = sortie_query.filter(difficulte_ressentie = difficulte)##on récupère uniquement les itinéraires avec la difficulté ressentie précisée
    
    if is_valid_query(duree_min):
        itineraire_query = itineraire_query.filter(duree__gte = duree_min)##vérifie que la durée estimée de l'itinéraire est supérieure ou égale à la durée précisée
        sortie_query = sortie_query.filter(duree_reelle__gte=duree_min)    ##vérifie que la durée réelle de la sortie est supérieure ou égale à la durée précisée
                          
    if is_valid_query(duree_max):
        itineraire_query = itineraire_query.filter(duree__lte = duree_max) ##vérifie que la durée estimée de l'itinéraire est inférieure ou égale à la durée précisée
        sortie_query = sortie_query.filter(duree_reelle__lte=duree_max)   ##vérifie que la durée réelle de la sortie est inférieure ou égale à la durée précisée
    
    return render(request, "itineraires/search_form.html", {'recherche': query, 'qs': sortie_query, 'qi': itineraire_query, 'difficulte': difficulte,'duree_min': duree_min, 'duree_max': duree_max})
    

@login_required
def ajout_commentaire(request, sortie_id):
    """
    Ajoute un commentaire sous une sortie.
    Args:
        request : la demande entrante, GET or POST
        sortie_id : l'identifiant de la sortie à modifier
    Returns:
        - Une page avec une boîte commentaire à remplir pour l'envoyer dans l'espace commentaire de la sortie associée.
    """
    
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

@login_required
def photo_upload(request, sortie_id):
    """
    Args:
        request : la demande entrante, GET or POST
        sortie_id : l'identifiant de la sortie à modifier
    Returns:
        - Une page avec un bouton de téléchargement d'une photo. Celle-ci apparaîtra alors sur la page de la sortie associée.
    """
    
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


