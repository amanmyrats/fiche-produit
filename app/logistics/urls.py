from django.urls import path

from logistics.views import logistics_view, LogisticsListView, facture_create_view, FactureListView, FactureDetailView, facture_edit_view


urlpatterns = [
    path('', LogisticsListView.as_view(), name='logistics'),
    path('factures/', FactureListView.as_view(), name = 'facturelist'),
    path('factures/<int:pk>/', FactureDetailView.as_view(), name = 'facturedetail'),
    path('factures/create/', facture_create_view, name = 'facturecreate'),
    path('factures/<int:pk>/edit/', facture_edit_view, name = 'factureedit'),
]