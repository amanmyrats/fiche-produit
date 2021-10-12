from fiche_produit.models import Product, ProductCard
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
import requests
import json
from django.template.response import TemplateResponse
from requests.api import get
from openpyxl import Workbook, load_workbook
from pathlib import Path
from django.conf import settings
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import shutil

from .forms import ProductModelForm, FPModelForm
from .utility import fp_excel_works, fp_pdf_works, download
# Create your views here.
mysitedomain = 'http://127.0.0.1:8000/'

def home_view(request):
    return render(request, 'home.html', {'msg': 'Hello Home'})

def site_view(request):
    apidata = requests.get(url=mysitedomain + 'api/fps/')
    context={'apidata': apidata.json()}
    return render(request, 'site/site.html', context)

def achat_view(request):
    return render(request, 'achat/achat.html', {'msg': 'Hello Home'})

def logistics_view(request):
    return render(request, 'logistics/logistics.html', {'msg': 'Hello Home'})

def qs_view(request):
    return render(request, 'qs/qs.html', {'msg': 'Hello Home'})

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

    if request.method=='POST':
        form = FPModelForm(request.POST)
        if form.is_valid():
            api_create_fp = mysitedomain + 'api/fps/'
            create_request = requests.post(url = api_create_fp, data = request.POST)
            response =create_request.json()
            print('this is response from api request:', response)
            print(response['id'])
            print(create_request.status_code)
            context = {'success': 'FP has been created, you are now redirected to products list.'}
            return redirect('/site/')
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
        form = ProductModelForm(request.POST)
        if form.is_valid():
            api_create_product = mysitedomain + 'api/products/'
            create_request = requests.post(url = api_create_product, data = request.POST)
            response =create_request.json()
            print(response['id'])
            print(create_request.status_code)
            context = {'success': 'Product has been submitted, you are now redirected to products list.'}  
            return redirect('/products/')
        else:
            product_form = form
            context={'product_form': product_form}
            context['errors']=form.errors

    return render(request, 'site/productform.html', context)

def test_view(request):
    pass