from fiche_produit.models import Product
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
import requests
import json
from django.template.response import TemplateResponse
from requests.api import get
from openpyxl import Workbook, load_workbook
from pathlib import Path
from django.conf import settings

from .forms import ProductModelForm

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

    print(what, towhat, pk)
    fp = requests.get(url=mysitedomain + 'api/fps/{}/'.format(pk))
    fp =fp.json()

    
    if what == 'fp' and towhat == 'excel':
        print('inside excel if')
        excel_path = Path(settings.MEDIA_ROOT) / 'excel_template' / 'fp.xlsx'
        wb = load_workbook(excel_path)
        print('wb created successfully')
        sh = wb['Fiche technique']
        print(sh.title)
        for cl in wb.defined_names:
            print('defined names:',cl, wb.defined_names[cl])
        
        wb.save(excel_path)
        wb.close()
        file = open(excel_path, "rb")
        response = HttpResponse(file.read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
        return response

    context={'fp': fp}

    return render(request, 'qs/qs.html', context)

def fpcreate_view(request):
    if request.method=='GET':
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, pk = product_id)
        context = {'product': product}
        return render(request, 'site/fpform.html', context)
    else:
        context = {'success': 'FP has been submitted, you are now redirected to products list.'}
        return redirect('/site/')

def products_view(request):
    products = requests.get(url=mysitedomain + 'api/products/')
    return render(request, 'site/products.html', {'products': products.json()})

def product_create_view(request):

    if request.method=='GET':
        product_form = ProductModelForm()
        context={'product_form': product_form}
        return render(request, 'site/productform.html', context)
    else:
        context = {'success': 'Product has been submitted, you are now redirected to products list.'}
        return redirect('/products/')

