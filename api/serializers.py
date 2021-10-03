from django.db.models import fields
from django.db.models.query_utils import select_related_descend
from fiche_produit.models import Product, ProductCard
from django.db import models
from rest_framework import serializers

class FPModelSerializer(serializers.ModelSerializer):
    order_numbers = serializers.CharField()
    facture_numbers = serializers.CharField()
    specification_numbers = serializers.CharField()
    tds_numbers = serializers.CharField()
    declaration_numbers = serializers.CharField()
    coo_numbers = serializers.CharField()
    product_name = serializers.CharField()
    image_url = serializers.CharField()

    class Meta:
        model = ProductCard
        fields = '__all__'


class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name_fr']


class QueueSerializer(serializers.Serializer):
    pass