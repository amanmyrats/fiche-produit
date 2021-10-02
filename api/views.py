from rest_framework import generics

from fiche_produit.models import Product, ProductCard
from .serializers import FPModelSerializer, ProductModelSerializer

class FPListAPIView(generics.ListAPIView):
    queryset = ProductCard.objects.all()
    serializer_class = FPModelSerializer

class ProductListAPIView (generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer

