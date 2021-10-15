from os import stat
from django.http import response
import requests

from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse

from rest_framework  import status

from .forms import   OrderItemModelForm, OrderModelForm
from fiche_produit.models import Order



mysitedomain = 'http://127.0.0.1:8000/'

def hgcreate_view(request):
    orderform = OrderModelForm
    if request.method=='POST':
        orderform = OrderModelForm(request.POST)
        url = mysitedomain + 'api/orders/'
        data = request.POST
        print('data to be sent:', data)
        hgcreate_request = requests.post(url=url, data = data)
        response =hgcreate_request.json()
        if status.is_success(hgcreate_request.status_code):
            print('response:', response)
            new_hg_id = response.get('id')
            print('hg response', response)
            print('new id', new_hg_id)

            return redirect('/hg/{}/additem/'.format(new_hg_id))
            # return HttpResponseRedirect(reverse('hgadditem', kwargs={'pk', new_hg_id}))
    context = {
        'orderform':orderform,
    }
    return render(request, 'achat/hgform.html', context)

def hgadditem_view(request, **kwargs):
    current_order_id = pk=kwargs['pk']
    order = get_object_or_404(Order, pk=current_order_id)
    existing_items = order.orderorderitems.all()
    orderitemform = OrderItemModelForm

    if request.method=='POST':
        orderitemform = OrderItemModelForm(request.POST)
        url = mysitedomain + 'api/orderitems/'.format(current_order_id)
        data = request.POST.copy()
        data['order']=current_order_id
        hg_additem_request = requests.post(url = url, data=data)
        print('hg_additem_request response', hg_additem_request)
        if status.is_success(hg_additem_request.status_code):
            return redirect('/hg/{}/additem/'.format(current_order_id))

    context = {
        'order':order,
        'existing_items':existing_items,
        'orderitemform':orderitemform
    }
    return render(request, 'achat/hgitemform.html', context)

