from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
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
def nouvelle_sortie(request):
    """
    Crée une nouvelle sortie dans la base de donnée
    Args:
        request: la demande entrante, GET or POST
    Returns:
        - Une page avec un formulaire vide si c'est une requête GET,
        - Une page avec un formulaire pré-rempli si c'est une requête POST
          avec des mauvaises donnée,
        - ou une page avec la sortie ajouté
    """
    if request.method == 'GET':
         form = SortieForm()
    elif request.method == "POST":
        form = SortieForm(request.POST)
        if form.is_valid():
            sortie = form.save(commit=False)
            sortie.author = request.user
            sortie.published_date = timezone.now()
            sortie.save()
            return redirect('itineraires:sortie_details', pk = sortie.pk)
    return render(request, 'itineraires/modif_sortie.html', {'form': form})

@login_required
def modif_sortie(request, sortie_id):
    """
    Modifie uen sortie déjà enregistée dans la base de donnée
    Args:
        request: la demande entrante, GET or POST
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
            sortie.author = request.user
            sortie.published_date = timezone.now()
            sortie.save()
            return redirect('itineraires:sortie_details', sortie_id)
    return render(request, 'itineraires/modif_sortie.html', {'form': form})



