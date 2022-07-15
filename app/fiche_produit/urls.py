from django.urls import path

from fiche_produit.views import home_view, SiteListView, SiteFilterView, export_view, fpcreate_view, products_view, \
                                product_create_view, fpchange_view, fpedit_view, fpprint_view, FPListView, FPDetailView, SiteListView,\
                                    test_view

urlpatterns = [
        path('', SiteListView.as_view(), name='site'),
        path('fps/', FPListView.as_view(), name='fplist'),
        path('fps/<int:pk>/', FPDetailView.as_view(), name='fpdetail'),
        path('fps/create/', fpcreate_view, name='fpcreate'),
        path('fps/<int:pk>/change/', fpchange_view, name='fpchange'),
        path('fps/<int:pk>/edit/', fpedit_view, name='fpedit'),
        path('fps/<int:pk>/print/', fpprint_view, name='fpprint'),
        path('products/', products_view, name='products'),
        path('products/create/', product_create_view, name='product-create'),
    ]