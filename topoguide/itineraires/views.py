from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .forms import SortieForm
from .models import Itineraire, Sortie

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
    return render(request, 'itineraires/sorties_details.html', {'sortie': sortie})


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
    return render(request, 'itineraires/modif_sortie.html', {'form': form, 'itineraire' : sortie.itineraire})

def is_valid_query(param):
    return param != '' and param is not None


def SearchView(request):
    itineraire_query = Itineraire.objects.all()
    sortie_query = Sortie.objects.all()
    query = request.GET.get('barre_recherche')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    
    if is_valid_query(query):
        itineraire_query = itineraire_query.filter(Q(titre__icontains = query)  | ##on cherche dans le titre de l'itinéraire
                                                   Q(description__icontains = query) | ## ou dans la description de l'itinéraire
                                                   Q(point_depart__icontains = query)) ## ou dans le nom du point de départ
        sortie_query = sortie_query.filter(Q(utilisateur__username__icontains = query) |
                                           Q(itineraire__titre__icontains = query))
    
    
    if is_valid_query(date_min):
        sortie_query = sortie_query.filter(date_sortie__gte=date_min)                                       

    
    if is_valid_query(date_max):
        sortie_query = sortie_query.filter(date_sortie__lt=date_max)                                       

    
    
    return render(request, "itineraires/search_form.html", {'recherche': query, 'qs': sortie_query, 'qi': itineraire_query})


