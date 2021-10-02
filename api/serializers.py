from fiche_produit.models import Product, ProductCard
from django.db import models
from rest_framework import serializers

class FPModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCard
        fields = ['product', 'project', 'no']

class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name_fr']