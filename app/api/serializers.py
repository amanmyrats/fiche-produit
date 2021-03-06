from rest_framework import serializers

from django.db.models.query_utils import select_related_descend
from fiche_produit.models import FactureItem, OrderItem, Product, ProductCard, Order, Facture, OrderItem, FactureItem, Specification, \
    SpecificationItem, Facture, Specification, Declaration, DeclarationItem, TdsItem, Tds, CooFacture, Coo, \
        RoutageItem, Routage, ProductCardAnnexe5, ProductCardRoom


class OrderModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class FPModelSerializer(serializers.ModelSerializer):
    order_numbers = serializers.CharField(read_only=True)
    facture_numbers = serializers.CharField(read_only=True)
    specification_numbers = serializers.CharField(read_only=True)
    tds_numbers = serializers.CharField(read_only=True)
    declaration_numbers = serializers.CharField(read_only=True)
    coo_numbers = serializers.CharField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    product_name_fr = serializers.CharField(read_only=True)
    product_name_ru = serializers.CharField(read_only=True)
    product_desc_fr = serializers.CharField(read_only=True)
    product_desc_ru = serializers.CharField(read_only=True)
    image_url = serializers.CharField(read_only=True)
    productcardorderitems = OrderItemModelSerializer(many = True, read_only =True)

    class Meta:
        model = ProductCard
        fields = '__all__'


class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class OrderModelSerializer(serializers.ModelSerializer):
    facture_numbers = serializers.CharField(read_only=True)
    specification_numbers = serializers.CharField(read_only=True)
    tds_numbers = serializers.CharField(read_only=True)
    declaration_numbers = serializers.CharField(read_only=True)
    coo_numbers = serializers.CharField(read_only=True)
    orderorderitems = OrderItemModelSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class FactureItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactureItem
        fields = '__all__'


class FactureModelSerializer(serializers.ModelSerializer):
    factureitems = FactureItemModelSerializer(many=True, read_only=True)
    class Meta:
        model = Facture
        fields = '__all__'

    
class SpecificationItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationItem
        fields = '__all__'


class SpecificationModelSerializer(serializers.ModelSerializer):
    specificationitems = SpecificationItemModelSerializer(many=True, read_only=True)
    class Meta:
        model = Specification
        fields = ['number', 'specificationitems']


class DeclarationItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclarationItem
        fields = '__all__'


class DeclarationModelSerializer(serializers.ModelSerializer):
    declarationitems = DeclarationItemModelSerializer(many=True, read_only=True)
    class Meta:
        model = Declaration
        fields = ['number', 'declarationitems']


class TdsItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TdsItem
        fields = '__all__'


class TdsModelSerializer(serializers.ModelSerializer):
    tdsitems = TdsItemModelSerializer(many=True, read_only=True)
    class Meta:
        model = Tds
        fields = ['number', 'tdsitems']


class RoutageItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutageItem
        fields = '__all__'


class RoutageModelSerializer(serializers.ModelSerializer):
    # routageitems = RoutageItemModelSerializer(many=True, read_only=True)
    routagetoroutageitem = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Routage
        fields = ['number', 'routagetoroutageitem']


class CooFactureModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CooFacture
        fields = '__all__'


class CooModelSerializer(serializers.ModelSerializer):
    cootofacture = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Coo
        fields = ['number', 'cootofacture']
    

class ProductCardAnnexe5ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCardAnnexe5
        fields = '__all__'


class FPNewNumberSerializer(serializers.Serializer):
    new_number = serializers.CharField()


