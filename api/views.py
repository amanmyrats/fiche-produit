from rest_framework import generics, mixins, viewsets
from rest_framework import filters
import django_filters.rest_framework
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from fiche_produit.models import Employee, Product, ProductCard
from .serializers import FPModelSerializer, ProductModelSerializer


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


# class FPListCreateAPIView(generics.ListCreateAPIView):
#     queryset = ProductCard.objects.all()
#     serializer_class = FPModelSerializer
#     filter_backends =[filters.SearchFilter, ]
#     search_fields = ['number','product__name_fr', 'provider__name_fr','origin__name_fr','project__code','department__name','lot__name_fr','lot__number']
#     # filterset_fields = ['provider','origin','project','department','lot']

#     def get_queryset(self):
#         project = self.request.query_params.get('project')
#         department = self.request.query_params.get('department')
#         trade = self.request.query_params.get('trade')
#         lot = self.request.query_params.get('lot')
#         provider = self.request.query_params.get('provider')
#         employee = self.request.query_params.get('employee')

#         filtered_fps = ProductCard.objects.all()
#         if project:
#             print('filtering project:', project)
#             filtered_fps = filtered_fps.filter(project=project)
#         if department:
#             filtered_fps = filtered_fps.filter(department=department)
#         if trade:
#             filtered_fps = filtered_fps.filter(trade=trade)
#         if lot:
#             filtered_fps = filtered_fps.filter(lot=lot)
#         if provider:
#             filtered_fps = filtered_fps.filter(provider=provider)
#         if employee:
#             filtered_fps = filtered_fps.filter(employee=employee)

#         return filtered_fps


# class FPRetrieveAPIView (generics.RetrieveAPIView):
#     queryset = ProductCard.objects.all()
#     serializer_class = FPModelSerializer

#     def get_object(self):
#         return get_object_or_404(self.queryset, pk=self.kwargs['pk'])



# class ProductListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer


# class ProductRetrieveAPIView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer

#     def get_object(self):
#         return get_object_or_404(self.queryset, pk=self.kwargs['pk'])