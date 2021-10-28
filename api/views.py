from django.db.models.query import QuerySet
from rest_framework import generics, mixins, viewsets
from rest_framework import filters
import django_filters.rest_framework
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404

from fiche_produit.models import Employee, Product, ProductCard, Order, Facture, ProductCardAnnexe5, Project, Specification, Declaration, Tds, Coo, Routage, \
    OrderItem, FactureItem, Lot
from .serializers import FPModelSerializer, ProductModelSerializer, OrderModelSerializer, FactureModelSerializer, \
    SpecificationModelSerializer, DeclarationModelSerializer, TdsModelSerializer, CooModelSerializer, RoutageModelSerializer, \
        RoutageModelSerializer, OrderItemModelSerializer, FactureItemModelSerializer, FPNewNumberSerializer, \
            ProductCardAnnexe5ModelSerializer


class EnablePartialUpdateMixin:
    """Enable partial updates

    Override partial kwargs in UpdateModelMixin class
    https://github.com/encode/django-rest-framework/blob/91916a4db14cd6a06aca13fb9a46fc667f6c0682/rest_framework/mixins.py#L64
    """
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class FPViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    queryset = ProductCard.objects.all()
    serializer_class = FPModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number','product__name_fr', 'provider__name_fr','origin__name_fr',
                        'project__code','department__name','lot__name_fr','lot__number']
    filter_fields = ['provider','origin','project','department','lot']


class ProductViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['name_en', 'name_fr','name_ru', 'name_tm', 'desc_en', 'desc_fr', 'desc_ru', 'desc_tm', 'created_by__name_en']
    filter_fields = ['created_by__name_en']


class OrderViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number', 'project']
    filter_fields = ['project']


class OrderItemViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['order__number', 'desc_fr']
    filter_fields = ['order__number']


class FactureViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    queryset = Facture.objects.all()
    serializer_class = FactureModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number', 'project']
    filter_fields = ['project']


class FactureItemViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    queryset = FactureItem.objects.all()
    serializer_class = FactureItemModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['facture__number']
    filter_fields = ['facture__number']


class SpecificationViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number', 'project']
    filter_fields = ['number']


class DeclarationViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    queryset = Declaration.objects.all()
    serializer_class = DeclarationModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number', 'project']
    filter_fields = ['number']


class TdsViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    queryset = Tds.objects.all()
    serializer_class = TdsModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number', 'project']
    filter_fields = ['number']


class CooViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    queryset = Coo.objects.all()
    serializer_class = CooModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number']
    filter_fields = ['number']


class RoutageViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    queryset = Routage.objects.all()
    serializer_class = RoutageModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['number']
    filter_fields = ['number']


class ProductCardAnnexe5ViewSet(viewsets.ModelViewSet):
    queryset = ProductCardAnnexe5.objects.all()
    serializer_class = ProductCardAnnexe5ModelSerializer
    filter_backends =[filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['productcard', 'annexe5', 'quantity']
    filter_fields = ['productcard', 'annexe5', 'quantity']


def fp_number_generator(request):
    lot_id = request.GET.get('lot_id')
    project_id = request.GET.get('project_id')
    number_type = request.GET.get('number_type')
    new_fp_number =''
    if number_type == 'fp':
        try:
            lot = Lot.objects.get(id=lot_id)
            project = Project.objects.get(id=project_id)
            print('lot', lot)
            allfp = ProductCard.objects.filter(lot=lot, project=project).values('number')
            print('allfp', allfp)
            if not len(allfp):
                new_fp_number = str(lot.number)[:2] + str('001')
            else:
                print('generating number')
                existing_numbers = [fp['number'] for fp in allfp]
                existing_numbers.sort()
                new_number = int(str(existing_numbers[-1])[-4:]) + 1
                new_fp_number = str(lot.number)[:2] + str(((3-len(str(new_number)))*'0')) + str(new_number)
        except:
            new_fp_number = ''


    data={'new_number' : new_fp_number}
    number = FPNewNumberSerializer(data)

    return JsonResponse(number.data, safe=False)
