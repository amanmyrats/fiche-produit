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
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from fiche_produit.views import home_view, site_view, achat_view, logistics_view, qs_view, export_view, fpcreate_view, products_view, \
                                product_create_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('site/', site_view, name='site'),
    path('/fps/create/', fpcreate_view, name='fpcreate'),
    path('achat/', achat_view, name='achat'),
    path('logistics/', logistics_view, name='logistics'),
    path('qs/', qs_view, name='qs'),
    path('export/', export_view, name='export'),
    path('products/', products_view, name='products'),
    path('products/create/', product_create_view, name='product-create'),
    path('', include('api.urls')),
    # path('', include('api.urls'))
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

