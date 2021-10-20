from django.db import models
from django.db.models import fields
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.views import generic
import requests
import json

import django_filters
from django_filters.views import FilterView

from django.template.response import TemplateResponse
from rest_framework  import status
from requests.api import get
from openpyxl import Workbook, load_workbook
from pathlib import Path
from django.conf import settings
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import shutil

from fiche_produit.models import Product, ProductCard, Specification
from .forms import ProductModelForm, FPModelForm
from .utility import fp_excel_works, fp_pdf_works, download

mysitedomain = 'http://127.0.0.1:8000/'

def home_view(request):
    return render(request, 'home.html', {'msg': 'Hello Home'})


def export_view(request):
    what = request.GET.get('what')
    towhat = request.GET.get('towhat')
    pk = request.GET.get('pk')

    current_fp = ProductCard.objects.get(pk=pk)

    print(what, towhat, pk)
    fp_from_api = requests.get(url=mysitedomain + 'api/fps/{}/'.format(pk))
    fp_from_api =fp_from_api.json()

    if what == 'fp':
        print('inside excel if')
        
        shutil.copy(Path(settings.MEDIA_ROOT) / 'excel_template' / 'fp.xlsx', Path(settings.MEDIA_ROOT) / 'excel_template' / 'fp_temp.xlsx')
        excel_path = Path(settings.MEDIA_ROOT) / 'excel_template' / 'fp_temp.xlsx'
        parent_path = Path(settings.MEDIA_ROOT) / 'excel_template' 
        print('path of openpyxl', excel_path)
        # try:
        wb = load_workbook(excel_path)
        print('wb loaded successfully')
        sh = wb['Fiche technique']
        print(sh.title)
        # Call excel creator
        try:
            current_image = current_fp.product.image
            wb = fp_excel_works(wb=wb, sh=sh, data_dict=fp_from_api, image_path = current_fp.product.image)
        except:
            wb = fp_excel_works(wb=wb, sh=sh, data_dict=fp_from_api, image_path = '')
        print('excel has been returned')
        wb.save(excel_path)
        wb.close()
        # if towhat=='pdf':
        #     print('before download pdf')
        #     pdf_path = fp_pdf_works(excel_path=excel_path, sh_name=sh.title, parent_path= parent_path , file_name = fp_from_api.get('number'))
        #     # pdf_path= Path(settings.MEDIA_ROOT) / 'excel_template' / 'fp.pdf'
        #     print('returned from pdf function', pdf_path)
        #     wrapper = FileWrapper(open(pdf_path, 'rb'))
        #     response = HttpResponse(wrapper, content_type='application/force-download')
        #     response['Content-Disposition'] = 'attachment; filename=' + fp_from_api.get('number') + '.pdf'
        #     return response

        if towhat=='excel':
            file = open(excel_path, "rb")
            response = HttpResponse(file.read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            if len(fp_from_api.get('number'))>0:
                response['Content-Disposition'] = 'attachment; filename=' + fp_from_api.get('number') + '.xlsx'
            else:
                response['Content-Disposition'] = 'attachment; filename=No-Number.xlsx'
            return response
        # except:
        #     try:
        #         wb.close()
        #     except:
        #         pass

        
        return redirect('/site/')


def fpcreate_view(request):
    product_id = request.GET.get('product_id')
    print('fp will created using product with as id:', product_id)
    product = get_object_or_404(Product, pk = product_id)
    form = FPModelForm({'product':product})
    context = {'form': form}
    context['submit_button_name'] = 'Add New Fiche Produit'

    if request.method=='POST':
        form = FPModelForm(request.POST)
        if form.is_valid():
            api_create_fp = mysitedomain + 'api/fps/'
            create_request = requests.post(url = api_create_fp, data = request.POST)
            response =create_request.json()
            print('this is response from api request:', response)
            print(create_request.status_code)
            if status.is_success(create_request.status_code):
                print(response['id'])
                context = {'success': 'FP has been created, you are now redirected to fp list.'}
                return redirect('/fps/')
            else:
                context['form'] = form
                context['errors'] = form.errors
        else:
            context['form'] = form
            context['errors'] = form.errors

    return render(request, 'site/fpform.html', context)

def fpchange_view(request, **kwargs):
    # fp_id = request.GET.get('fp_id')
    fp_id = kwargs.get('pk')
    print('fp will change fp with an id:', fp_id)
    fp = get_object_or_404(ProductCard, pk = fp_id)
    form = FPModelForm(instance = fp)
    context = {'form': form}
    context['submit_button_name'] = 'Save Changes'

    if request.method=='POST':
        # form = FPModelForm(request.POST)
        # print('will check if form is valid')
        # if form.is_valid():
        #     print('form is valid')
        api_change_fp = mysitedomain + 'api/fps/{}/'.format(fp_id)
        create_request = requests.patch(url = api_change_fp, data = request.POST)
        print(create_request.status_code)
        response =create_request.json()
        print('this is response from api request:', response)
        if status.is_success(create_request.status_code):
                print(response['id'])
                context = {'success': 'FP has been edited, you are now redirected to fp list.'}
                # Here it must be fp detail list with Kerim's template
                return redirect('/fps/')

        else:
            context['form'] = form
            context['errors'] = form.errors

    return render(request, 'site/fpform.html', context)

def products_view(request):
    products = requests.get(url=mysitedomain + 'api/products/')
    return render(request, 'site/products.html', {'products': products.json()})

def product_create_view(request):
    product_form = ProductModelForm()
    context={'product_form': product_form}

    if request.method=='POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            api_create_product = mysitedomain + 'api/products/'
            create_request = requests.post(url = api_create_product, data = request.POST, files=request.FILES)
            print('status code:',create_request.status_code)
            response =create_request.json()
            print('respone:', response)
            print(response['id'])
            context = {'success': 'Product has been submitted, you are now redirected to products list.'}  
            return redirect('/products/')
        else:
            product_form = form
            context={'product_form': product_form}
            context['errors']=form.errors

    return render(request, 'site/productform.html', context)


def test_view(request, **kwargs):
    pass


def fpprint_view(request, **kwargs):
    fp_id = kwargs.get('pk')
    print('fp will print fiche produit with an id:', fp_id)
    fp = get_object_or_404(ProductCard, pk = fp_id)
    context = {'fp': fp}
    return render(request, 'site/fpprint.html', context)


class FPFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name = 'product__name_fr', lookup_expr = 'icontains')
    fpnumber = django_filters.CharFilter(field_name = 'number', lookup_expr = 'icontains')
    order = django_filters.CharFilter(field_name = 'productcardorderitems__order__number', lookup_expr = 'icontains')
    facture = django_filters.CharFilter(field_name = 'productcardorderitems__orderitemsinfactureitems__facture__number', lookup_expr = 'icontains')
    specification = django_filters.CharFilter(field_name = 'productcardorderitems__orderitemsinfactureitems__specificationfactures__specification__number', lookup_expr = 'icontains')
    tds  = django_filters.CharFilter(field_name = 'productcardorderitems__orderitemsinfactureitems__tdsfactures__tds__number', lookup_expr = 'icontains')
    declaration  = django_filters.CharFilter(field_name = 'productcardorderitems__orderitemsinfactureitems__declarationfactures__declaration_number', lookup_expr = 'icontains')
    coo  = django_filters.CharFilter(field_name = 'productcardorderitems__orderitemsinfactureitems__facturetocoo__coo__number', lookup_expr = 'icontains')

    class Meta:
        model = ProductCard
        fields = ['project', 'trade', 'lot', 'annexe5']


class SiteFilterView(FilterView):
    model = ProductCard
    context_object_name  = 'fps'
    template_name = 'site/site.html'
    ordering = ['-created_at']
    filterset_class = FPFilter


class SiteListView(generic.ListView):
    model = ProductCard
    context_object_name = 'fps'
    template_name = 'site/site.html'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super(SiteListView, self).get_context_data(**kwargs)
        # context['filter'] = FPFilter(self.request.GET, queryset = self.get_queryset())
        return context
    
    def get_queryset(self):
        queryset = super(SiteListView, self).get_queryset()
        return set(FPFilter(self.request.GET, queryset = queryset).qs)


class FPListView(generic.ListView):
    model = ProductCard
    context_object_name  = 'fps'
    template_name = 'site/fplist.html'
    ordering = ['-created_at']


# class SiteListView(generic.ListView):
#     model = ProductCard
#     context_object_name  = 'fps'
#     template_name = 'site/site.html'
#     ordering = ['-created_at']


class FPDetailView(generic.DetailView):
    queryset = ProductCard.objects.all()
    context_object_name  = 'fps'
    template_name = 'site/fpdetail.html'