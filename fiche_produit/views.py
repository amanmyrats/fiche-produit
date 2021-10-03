from django.shortcuts import render
import requests
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


