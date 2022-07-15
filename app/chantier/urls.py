from django.urls import path 

from .views import chantier_home

urlpatterns = [ 
    path('', chantier_home, name='chantier')
]