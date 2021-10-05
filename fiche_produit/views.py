from django.shortcuts import render, HttpResponse
import requests
import json
from django.template.response import TemplateResponse

from openpyxl import Workbook, load_workbook
from pathlib import Path

from django.conf import settings

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


