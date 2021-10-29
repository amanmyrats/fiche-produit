"""fp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse

from django.conf import settings
from django.conf.urls.static import static


from fiche_produit.views import home_view, SiteListView, SiteFilterView, export_view, fpcreate_view, products_view, \
                                product_create_view, fpchange_view, fpedit_view, fpprint_view, FPListView, FPDetailView, SiteListView
from achat.views import achat_view, order_create_view, AchatListView, OrderListView, OrderDetailView, order_edit_view
from logistics.views import logistics_view, LogisticsListView, facture_create_view, FactureListView, FactureDetailView, facture_edit_view
from qs.views import qs_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # path('accounts/login/', auth_views.LoginView.as_view(template_name = 'registration/login.html', success_url='home'), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(template_name='home.html', next_page='home'), name='logout'),
    # path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html',success_url='/?passwordchanged=1'), name='password_change'),
    
    path('site/', SiteListView.as_view(), name='site'),
    path('fps/', FPListView.as_view(), name='fplist'),
    path('fps/<int:pk>/', FPDetailView.as_view(), name='fpdetail'),
    path('fps/create/', fpcreate_view, name='fpcreate'),
    path('fps/<int:pk>/change/', fpchange_view, name='fpchange'),
    path('fps/<int:pk>/edit/', fpedit_view, name='fpedit'),
    path('fps/<int:pk>/print/', fpprint_view, name='fpprint'),

    path('achat/', AchatListView.as_view(), name='achat'),
    path('orders/', OrderListView.as_view(), name = 'orderlist'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name = 'orderdetail'),
    path('orders/create/', order_create_view, name = 'ordercreate'),
    path('orders/<int:pk>/edit/', order_edit_view, name = 'orderedit'),

    path('logistics/', LogisticsListView.as_view(), name='logistics'),
    path('factures/', FactureListView.as_view(), name = 'facturelist'),
    path('factures/<int:pk>/', FactureDetailView.as_view(), name = 'facturedetail'),
    path('factures/create/', facture_create_view, name = 'facturecreate'),
    path('factures/<int:pk>/edit/', facture_edit_view, name = 'factureedit'),

    path('qs/', qs_view, name='qs'),
    path('export/', export_view, name='export'),
    path('products/', products_view, name='products'),
    path('products/create/', product_create_view, name='product-create'),

    path('', include('api.urls')),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

