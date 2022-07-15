from django.db import models
from django.db.models import fields
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.views import generic
from django.urls import reverse
import requests
import json

import django_filters
from django_filters.views import FilterView

from django.db.models import Q
from django.template.response import TemplateResponse
from rest_framework  import status
from requests.api import get
from openpyxl import Workbook, load_workbook
from pathlib import Path
from django.conf import settings
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import shutil
 # pywin32
# import win32com.client as win32
# import pythoncom
import tempfile
import os


from fiche_produit.models import Order, Product, ProductCard, Specification, ProductCardRoom, ProductCardAnnexe5
from .forms import ProductModelForm, FPModelForm, ProductCardAnnexe5ModelForm, ProductCardRoomModelForm
from .utility import fp_excel_works, fp_pdf_works, download, fp_excel_works_pywin32

mysitedomain = 'http://127.0.0.1:8000'

def home_view(request):
    return render(request, 'home.html', {'msg': 'Hello Home'})


def export_view(request):
    what = request.GET.get('what')
    towhat = request.GET.get('towhat')
    pk = request.GET.get('pk')

    current_fp = ProductCard.objects.get(pk=pk)

    print(what, towhat, pk)
    # fp_from_api = requests.get(url=mysitedomain + 'api/fps/{}/'.format(pk))
    fp_from_api = requests.get(url = request.build_absolute_uri(reverse('api:fps', kwargs={'pk', pk})))
    fp_from_api =fp_from_api.json()

    if what == 'fp':
        print('inside excel if')
        
        shutil.copy(Path(settings.MEDIA_ROOT) / 'excel_template' / 'fp.xlsx', Path(settings.MEDIA_ROOT) / 'excel_template' / 'fp_temp.xlsx')
        excel_path = Path(settings.MEDIA_ROOT)  / 'excel_template' / 'fp_temp.xlsx'
        parent_path = Path(settings.MEDIA_ROOT) / 'excel_template' 
        
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

        return redirect('/site/')


def fpcreate_view(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, pk = product_id)
    form = FPModelForm({'product':product})
    context = {'form': form}
    context['submit_button_name'] = 'Add New Fiche Produit'

    if request.method=='POST':
        form = FPModelForm(request.POST)
        if form.is_valid():
            create_request = requests.post(url = request.build_absolute_uri(reverse('api:fps-list')) , data = request.POST)
            response =create_request.json()
            print('this is response from api request:', response)
            if status.is_success(create_request.status_code):
                print(response['id'])
                context = {'success': 'FP has been created, you are now redirected to fp edit page.'}
                return redirect(reverse('fpedit',kwargs={'pk':response['id']}))
            else:
                context['form'] = form
                context['errors'] = form.errors
        else:
            context['form'] = form
            context['errors'] = form.errors

    return render(request, 'site/fpform.html', context)

def fpchange_view(request, **kwargs):
    fp_id = kwargs.get('pk')
    fp = get_object_or_404(ProductCard, pk = fp_id)
    form = FPModelForm(instance = fp)
    context = {'form': form}
    context['submit_button_name'] = 'Save Changes'

    if request.method=='POST':
        # create_request = requests.patch(url = mysitedomain + reverse('api:fps-list', fp_id), data = request.POST)
        create_request = requests.patch(url = request.build_absolute_uri(reverse('api:fps-list', fp_id)), data = request.POST)
        response =create_request.json()
        if status.is_success(create_request.status_code):
                print(response['id'])
                context = {'success': 'FP has been edited, you are now redirected to fp list.'}
                # Here it must be fp detail list with Kerim's template
                return redirect(reverse('fplist'))

        else:
            context['form'] = form
            context['errors'] = form.errors

    return render(request, 'site/fpform.html', context)



def fpedit_view(request, **kwargs):
    fp_id = kwargs.get('pk')
    fpannexe5_id = request.GET.get('fpannexe5')
    fproom_id = request.GET.get('fproom')

    # Objects
    fp = get_object_or_404(ProductCard, pk = fp_id)
    productcardannexe5s = ProductCardAnnexe5.objects.filter(productcard = fp)
    productcardrooms = ProductCardRoom.objects.filter(productcard = fp)
    fp_submit_button_name = 'Save Changes'

    # Forms
    fp_form = FPModelForm(instance = fp)
    if request.GET.get('editannexe5'):
        productcardannexe5_to_edit_id = request.GET.get('editannexe5')
        productcardannexe5_to_edit = ProductCardAnnexe5.objects.get(id=productcardannexe5_to_edit_id)
        fpannexe5_form = ProductCardAnnexe5ModelForm(instance=productcardannexe5_to_edit) 
        annexe5_submit_button_name = 'Save Changes'
    else:
        fpannexe5_form = ProductCardAnnexe5ModelForm()
        annexe5_submit_button_name = 'Add New Annexe5'

    if request.GET.get('editroom'):
        productcardroom_to_edit_id = request.GET.get('editroom')
        productcardroom_to_edit = ProductCardRoom.objects.get(id=productcardroom_to_edit_id)
        fproom_form = ProductCardRoomModelForm(instance=productcardroom_to_edit) 
        room_submit_button_name = 'Save Changes'
    else:
        fproom_form = ProductCardRoomModelForm()
        room_submit_button_name = 'Add New Room'

    context = {'fp_form': fp_form}
    context['fpannexe5_form'] = fpannexe5_form
    context['fproom_form'] = fproom_form
    context['fp'] = fp
    context['productcardrooms'] = productcardrooms
    context['productcardannexe5s'] = productcardannexe5s
    context['annexe5_submit_button_name'] = annexe5_submit_button_name
    context['room_submit_button_name'] = room_submit_button_name
    context['fp_submit_button_name'] = fp_submit_button_name

    if request.method=='POST':
        # print(request.GET.get('editfp'))
        # print(request.GET.get('addannexe5'))
        # print(request.GET.get('editannexe5'))
        # print(request.GET.get('addroom'))
        # print(request.GET.get('editroom'))
        if request.GET.get('editfp'):
            create_request = requests.patch(url = request.build_absolute_uri(reverse('api:fps-detail', kwargs={'pk':fp_id})), data = request.POST)
            # print(create_request.status_code)
            response =create_request.json()
            # print('this is response from api request:', response)
            if status.is_success(create_request.status_code):
                    print(response['id'])
                    context = {'success': 'FP has been edited, you are now redirected to fp list.'}
                    # Here it must be fp detail list with Kerim's template

        if request.GET.get('addannexe5'):
            fpannexe5_form = ProductCardAnnexe5ModelForm(request.POST)
            if fpannexe5_form.is_valid():
                annexe5 = request.POST.get('annexe5')
                quantity = request.POST.get('quantity')
                fp.annexe5s.add(annexe5, through_defaults={'quantity': quantity})
            else:
                context['errors'] = fpannexe5_form.errors

        if request.GET.get('editannexe5'):
            existing_productcardannexe5 = request.GET.get('editannexe5')
            new_annexe5 = request.POST.get('annexe5')
            new_quantity = request.POST.get('quantity')
            try:
                ProductCardAnnexe5.objects.filter(id=existing_productcardannexe5).update(annexe5=new_annexe5, quantity=new_quantity)
            except:
                context['errors'] = 'Error happened when updating Annexe-5.'
                
        if request.GET.get('addroom'):
            fproom_form = ProductCardRoomModelForm(request.POST)
            if fproom_form.is_valid():
                room = request.POST.get('room')
                quantity = request.POST.get('quantity')
                fp.rooms.add(room, through_defaults={'quantity': quantity})
            else:
                context['errors'] = fproom_form.errors
        
        if request.GET.get('editroom') or request.GET.get('deleteroom'):
            existing_productcardroom = request.GET.get('editroom')
            new_room = request.POST.get('room')
            new_quantity = request.POST.get('quantity')
            try:
                ProductCardRoom.objects.filter(id=existing_productcardroom).update(room=new_room, quantity=new_quantity)
            except:
                context['errors'] = 'Error happened when editing room.'

        return redirect(reverse('fpedit', kwargs={'pk':fp_id}))
    
    else:
        if request.GET.get('deleteannexe5'):
            productCardAnnexe5_id = request.GET.get('deleteannexe5')
            try:
                ProductCardAnnexe5.objects.get(id=productCardAnnexe5_id).delete()
            except:
                context['errors'] = 'Error happened when deleting Annexe5.'
        
        if request.GET.get('deleteroom'):
            room_to_delete = request.GET.get('deleteroom')
            try:
                ProductCardRoom.objects.filter(id=room_to_delete).delete()
            except:
                context['errors'] = 'Error happened when deleting room'

    return render(request, 'site/fpedit.html', context)

def products_view(request):
    products = requests.get(url=request.build_absolute_uri(reverse('api:products-list')))
    return render(request, 'site/products.html', {'products': products.json()})

def product_create_view(request):
    product_form = ProductModelForm()
    context={'product_form': product_form}

    if request.method=='POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            create_request = requests.post(url = request.build_absolute_uri(reverse('api:products-list')), data = request.POST, files=request.FILES)
            print('status code:',create_request.status_code)
            response =create_request.json()
            print('respone:', response)
            print(response['id'])
            context = {'success': 'Product has been submitted, you are now redirected to products list.'}  
            return redirect(reverse('products'))
        else:
            product_form = form
            context={'product_form': product_form}
            context['errors']=form.errors

    return render(request, 'site/productform.html', context)


def test_view(request, **kwargs):
    return render(request, 'fiche_produit/fiche_produit_print.html', {'test':'test'})


def fpprint_view(request, **kwargs):
    fp_id = kwargs.get('pk')
    print('fp will print fiche produit with an id:', fp_id)
    fp = get_object_or_404(ProductCard, pk = fp_id)
    context = {'fp': fp}
    return render(request, 'site/fpprint.html', context)


class FPFilter(django_filters.FilterSet):
    order = django_filters.CharFilter(field_name = 'productcardorderitems__order__number', lookup_expr = 'icontains')
    facture = django_filters.CharFilter(field_name = 'productcardorderitems__orderitemsinfactureitems__facture__number', lookup_expr = 'icontains')
    specification = django_filters.CharFilter(field_name = 'productcardorderitems__orderitemsinfactureitems__specificationfactures__specification__number', lookup_expr = 'icontains')
    tds  = django_filters.CharFilter(field_name = 'productcardorderitems__orderitemsinfactureitems__tdsfactures__tds__number', lookup_expr = 'icontains')
    declaration  = django_filters.CharFilter(field_name = 'productcardorderitems__orderitemsinfactureitems__declarationfactures__declaration_number', lookup_expr = 'icontains')
    coo  = django_filters.CharFilter(field_name = 'productcardorderitems__orderitemsinfactureitems__facturetocoo__coo__number', lookup_expr = 'icontains')

    class Meta:
        model = ProductCard
        fields = ['project', 'trade', 'lot', 'provider']


class FPCustomAdvancedSearch(django_filters.FilterSet):
    search = django_filters.CharFilter(method = 'search_everywhere', label='Search')

    class Meta:
        model = ProductCard
        fields = ['search']
    
    def search_everywhere(self, queryset, name, value):
        return ProductCard.objects.filter(
            Q(project__code__icontains=value) | Q(number__icontains=value) | Q(product__name_fr__icontains=value) | Q(product__name_ru__icontains=value) \
                 | Q(product__name_tm__icontains=value) | Q(product__name_en__icontains=value) | Q(lot__number__icontains=value) \
                      | Q(productcardorderitems__order__number__icontains=value) \
                          | Q(productcardorderitems__orderitemsinfactureitems__facture__number__icontains=value) \
                              | Q(productcardorderitems__orderitemsinfactureitems__specificationfactures__specification__number__icontains=value) \
                                  | Q(productcardorderitems__orderitemsinfactureitems__declarationfactures__declaration__number__icontains=value) \
                                      | Q(productcardorderitems__orderitemsinfactureitems__facturetocoo__coo__number__icontains=value)
        )


class FPCustomSearch(django_filters.FilterSet):
    search = django_filters.CharFilter(method = 'search_everywhere', label='Search')

    class Meta:
        model = ProductCard
        fields = ['search']
    
    def search_everywhere(self, queryset, name, value):
        return ProductCard.objects.filter(
            Q(project__code__icontains=value) | Q(number__icontains=value) | Q(product__name_fr__icontains=value) | Q(product__name_ru__icontains=value) \
                 | Q(product__name_tm__icontains=value) | Q(product__name_en__icontains=value) | Q(lot__number__icontains=value) \
                      | Q(provider__code__icontains=value) \
                           | Q(provider__name_fr__icontains=value)
        )


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
    paginate_by  = 3

    # def get_context_data(self, **kwargs):
    #     context = super(SiteListView, self).get_context_data(**kwargs)
    #     # context['filter'] = FPFilter(self.request.GET, queryset = self.get_queryset())
    #     return context
    
    def get_queryset(self):
        queryset = super(SiteListView, self).get_queryset()
        queryset = FPCustomAdvancedSearch(self.request.GET, queryset = queryset).qs
        return list(set(FPFilter(self.request.GET, queryset = queryset).qs))


class FPListView(generic.ListView):
    model = ProductCard
    context_object_name  = 'fps'
    template_name = 'site/fplist.html'
    ordering = ['-created_at']
    paginate_by  = 3

    def get_queryset(self):
        queryset = super(FPListView, self).get_queryset()
        queryset = FPCustomSearch(self.request.GET, queryset = queryset).qs
        return list(set(FPFilter(self.request.GET, queryset = queryset).qs))


class FPDetailView(generic.DetailView):
    queryset = ProductCard.objects.all()
    context_object_name  = 'fps'
    template_name = 'site/fpdetail.html'