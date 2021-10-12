from django.db.models.query import QuerySet
from rest_framework import generics, mixins, viewsets
from rest_framework import filters
import django_filters.rest_framework
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from fiche_produit.models import Employee, Product, ProductCard, Order, Facture, Specification, Declaration, Tds, Coo, Routage
from .serializers import FPModelSerializer, ProductModelSerializer, OrderModelSerializer, FactureModelSerializer, \
    SpecificationModelSerializer, DeclarationModelSerializer, TdsModelSerializer, CooModelSerializer, RoutageModelSerializer, \
        RoutageModelSerializer


class FPViewSet(viewsets.ModelViewSet):
    queryset = ProductCard.objects.all()
    serializer_class = FPModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number','product__name_fr', 'provider__name_fr','origin__name_fr',
                        'project__code','department__name','lot__name_fr','lot__number']
    filter_fields = ['provider','origin','project','department','lot']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['name_en', 'name_fr','name_ru', 'name_tm', 'desc_en', 'desc_fr', 'desc_ru', 'desc_tm', 'created_by__name_en']
    filter_fields = ['created_by__name_en']


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number', 'project']
    filter_fields = ['project']


class FactureViewSet(viewsets.ModelViewSet):
    queryset = Facture.objects.all()
    serializer_class = FactureModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number', 'project']
    filter_fields = ['project']


class SpecificationViewSet(viewsets.ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number', 'project']
    filter_fields = ['number']


class DeclarationViewSet(viewsets.ModelViewSet):
    queryset = Declaration.objects.all()
    serializer_class = DeclarationModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number', 'project']
    filter_fields = ['number']


class TdsViewSet(viewsets.ModelViewSet):
    queryset = Tds.objects.all()
    serializer_class = TdsModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number', 'project']
    filter_fields = ['number']


class CooViewSet(viewsets.ModelViewSet):
    queryset = Coo.objects.all()
    serializer_class = CooModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number']
    filter_fields = ['number']


class RoutageViewSet(viewsets.ModelViewSet):
    queryset = Routage.objects.all()
    serializer_class = RoutageModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number']
    filter_fields = ['number']
