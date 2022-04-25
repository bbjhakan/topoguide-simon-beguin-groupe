from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .import views

app_name = 'itineraires'
urlpatterns = [
    # ex: /itineraires/
    path('', views.itineraires, name='itineraires'),
    # ex: /itineraires/1/
    path('sorties/<int:itineraire_id>/', views.sorties, name='sorties'),
    # ex: /itineraires/sortie/3/
    path('sortie/<int:sortie_id>/', views.sortie, name='sortie_details'),
    # ex: /itineraires/nouvelle_sortie/1/
    path('nouvelle_sortie/<int:itineraire_id>/', views.nouvelle_sortie, name='nouvelle_sortie'),
    # ex: /itineraires/modif_sortie/2/
    path('modif_sortie/<int:sortie_id>/', views.modif_sortie, name='modif_sortie'),
    
    path('sortie/<int:sortie_id>/post_commentaire/' , views.ajout_commentaire, name='ajout_commentaire'),
    
    path('sortie/<int:sortie_id>/photo/', views.photo_upload, name = 'photo_upload')
    ] 