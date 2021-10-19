from os import stat
from django.http import response
import requests

from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from rest_framework  import status

from .forms import   OrderItemModelForm, OrderModelForm
from fiche_produit.models import Order



mysitedomain = 'http://127.0.0.1:8000/'


def achat_view(request):
    orders = Order.objects.all()
    context = {
        'orders':orders
    }
    return render(request, 'achat/achat.html', context)


class OrderListView(generic.ListView):
    model = Order
    context_object_name = 'orders' 
    template_name = 'achat/orderlist.html'

class OrderDetailView(generic.DeleteView):
    queryset = Order.objects.all()
    context_object_name = 'order' 
    template_name = 'achat/orderdetail.html'

def order_create_view(request):
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
            return redirect('/orders/{}/edit/'.format(new_hg_id))
    context = {
        'orderform':orderform,
    }
    return render(request, 'achat/orderform.html', context)

def order_edit_view(request, **kwargs):
    order_id = kwargs.get('pk')
    order = get_object_or_404(Order, pk=order_id)
    existing_items = order.orderorderitems.all().order_by('no')
    show_form = False
    buttonname = 'Save New Item'
    orderitemform = OrderItemModelForm
    item_id = request.GET.get('edititem')

    # Check if user wants to edit item or add new item
    if request.GET.get('edititem'):
        print('item_id', item_id)
        item = order.orderorderitems.get(pk = item_id)
        orderitemform = OrderItemModelForm(instance=item)
        buttonname = 'Save Edit'
        show_form = True
    elif request.GET.get('additem'):
        orderitemform = OrderItemModelForm
        show_form = True
        

    if request.method=='POST':
        orderitemform = OrderItemModelForm(request.POST)
        url_add = mysitedomain + 'api/orderitems/'
        url_patch = mysitedomain + 'api/orderitems/{}/'.format(item_id)
        data = request.POST.copy()
        data['order']=order_id

        if request.GET.get('additem'):
            order_add_item_request = requests.post(url = url_add, data=data)
        elif request.GET.get('edititem'):
            order_add_item_request = requests.patch(url = url_patch, data=data)

        print('order_add_item_request response', order_add_item_request)
        if status.is_success(order_add_item_request.status_code):
            return redirect('/orders/{}/edit/'.format(order_id))

    context = {
        'order':order,
        'existing_items':existing_items,
        'orderitemform':orderitemform,
        'buttonname':buttonname,
        'show_form':show_form
    }
    return render(request, 'achat/orderitemform.html', context)

# def order_edit_view(request, **kwargs):
#     order_id = kwargs.get('pk')
#     order = get_object_or_404(Order, pk=order_id)
#     existing_items = order.orderorderitems.all()
#     orderitemform = OrderItemModelForm
#     if request.method == 'POST':
#         pass
#     context = {
#         'order':order,
#         'existing_items':existing_items,
#         'orderitemform':orderitemform
#     }
#     return render(request, 'achat/orderitemform.html', context)