from os import stat
from django.http import response
import requests

from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from rest_framework  import status

from .forms import   FactureItemModelForm, FactureModelForm
from fiche_produit.models import Facture



mysitedomain = 'http://127.0.0.1:8000/'



def logistics_view(request):
    factures = Facture.objects.all()
    context = {
        'factures':factures
    }
    return render(request, 'logistics/logistics.html', context)


class FactureListView(generic.ListView):
    model = Facture
    context_object_name = 'factures' 
    template_name = 'logistics/facturelist.html'

class FactureDetailView(generic.DeleteView):
    queryset = Facture.objects.all()
    context_object_name = 'facture' 
    template_name = 'logistics/facturedetail.html'

def facture_create_view(request):
    factureform = FactureModelForm
    if request.method=='POST':
        factureform = FactureModelForm(request.POST)
        url = mysitedomain + 'api/factures/'
        data = request.POST
        print('data to be sent:', data)
        facture_create_request = requests.post(url=url, data = data)
        response =facture_create_request.json()
        if status.is_success(facture_create_request.status_code):
            print('response:', response)
            new_facture_id = response.get('id')
            print('facture response', response)
            print('new id', new_facture_id)
            return redirect('/factures/{}/edit/'.format(new_facture_id))
    context = {
        'factureform':factureform,
    }
    return render(request, 'logistics/factureform.html', context)

def facture_edit_view(request, **kwargs):
    facture_id = kwargs.get('pk')
    facture = get_object_or_404(Facture, pk=facture_id)
    existing_items = facture.factureitems.all().order_by('no')
    show_form = False
    buttonname = 'Save New Item'
    factureitemform = FactureItemModelForm
    item_id = request.GET.get('edititem')

    # Check if user wants to edit item or add new item
    if request.GET.get('edititem'):
        print('item_id', item_id)
        item = facture.factureitems.get(pk = item_id)
        factureitemform = FactureItemModelForm(instance=item)
        buttonname = 'Save Edit'
        show_form = True
    elif request.GET.get('additem'):
        factureitemform = FactureItemModelForm
        show_form = True
        

    if request.method=='POST':
        factureitemform = FactureItemModelForm(request.POST)
        url_add = mysitedomain + 'api/factureitems/'
        url_patch = mysitedomain + 'api/factureitems/{}/'.format(item_id)
        data = request.POST.copy()
        data['facture']=facture_id

        if request.GET.get('additem'):
            facture_add_item_request = requests.post(url = url_add, data=data)
        elif request.GET.get('edititem'):
            facture_add_item_request = requests.patch(url = url_patch, data=data)

        print('facture_add_item_request response', facture_add_item_request)
        if status.is_success(facture_add_item_request.status_code):
            return redirect('/factures/{}/edit/'.format(facture_id))


    context = {
        'facture':facture,
        'existing_items':existing_items,
        'factureitemform':factureitemform,
        'buttonname':buttonname,
        'show_form':show_form
    }
    return render(request, 'logistics/factureitemform.html', context)
