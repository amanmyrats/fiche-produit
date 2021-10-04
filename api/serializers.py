from django.db.models import fields
from django.db.models.query_utils import select_related_descend
from fiche_produit.models import Product, ProductCard
from django.db import models
from rest_framework import serializers

class FPModelSerializer(serializers.ModelSerializer):
    order_numbers = serializers.CharField(read_only=True)
    facture_numbers = serializers.CharField(read_only=True)
    specification_numbers = serializers.CharField(read_only=True)
    tds_numbers = serializers.CharField(read_only=True)
    declaration_numbers = serializers.CharField(read_only=True)
    coo_numbers = serializers.CharField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    image_url = serializers.CharField(read_only=True)

    class Meta:
        model = ProductCard
        fields = '__all__'


class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name_fr']


class QueueSerializer(serializers.Serializer):
    pass