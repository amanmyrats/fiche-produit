from os import stat
from django.http import response
import requests

from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from rest_framework  import status
import django_filters
from django.db.models import Q

from .forms import   OrderItemModelForm, OrderModelForm
from fiche_produit.models import Order



mysitedomain = 'http://127.0.0.1:8000/'


def achat_view(request):
    orders = Order.objects.all()
    context = {
        'orders':orders
    }
    return render(request, 'achat/achat.html', context)

def order_create_view(request):
    orderform = OrderModelForm
    if request.method=='POST':
        orderform = OrderModelForm(request.POST)
        url = mysitedomain + 'api/orders/'
        data = request.POST
        print('data to be sent:', data)
        hgcreate_request = requests.post(url=request.build_absolute_uri(reverse('api:orders-list')), data = data)
        response =hgcreate_request.json()
        if status.is_success(hgcreate_request.status_code):
            print('response:', response)
            new_hg_id = response.get('id')
            print('hg response', response)
            print('new id', new_hg_id)
            return redirect(reverse('orderedit', kwargs={'pk':new_hg_id}))
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
        data = request.POST.copy()
        data['order']=order_id

        if request.GET.get('additem'):
            order_add_item_request = requests.post(url = request.build_absolute_uri(reverse('api:orderitems-list')), data=data)
        elif request.GET.get('edititem'):
            order_add_item_request = requests.patch(url = request.build_absolute_uri(reverse('api:orderitems-detail', kwargs={'pk':item_id})), data=data)

        print('order_add_item_request response', order_add_item_request)
        if status.is_success(order_add_item_request.status_code):
            return redirect(reverse('orderedit', kwargs={'pk':order_id}))

    context = {
        'order':order,
        'existing_items':existing_items,
        'orderitemform':orderitemform,
        'buttonname':buttonname,
        'show_form':show_form
    }
    return render(request, 'achat/orderitemform.html', context)

class OrderFilter(django_filters.FilterSet):
    trade = django_filters.CharFilter(field_name = 'orderorderitems__product_card__trade')
    lot = django_filters.CharFilter(field_name = 'orderorderitems__product_card__lot')
    annexe5 = django_filters.CharFilter(field_name = 'orderorderitems__product_card__annexe5')
    provider  = django_filters.CharFilter(field_name = 'orderorderitems__product_card__provider')
    
    class Meta:
        model = Order
        fields = ['project']


class OrderCustomSearch(django_filters.FilterSet):
    search = django_filters.CharFilter(method = 'search_everywhere', label='Search')

    class Meta:
        model = Order
        fields = ['search']
    
    def search_everywhere(self, queryset, name, value):
        return Order.objects.filter(
            # Q(location__name_tm__icontains=value)
            Q(project__code__icontains=value) | Q(number__icontains=value) \
                | Q(orderorderitems__product_card__product__name_en__icontains=value) \
                | Q(orderorderitems__product_card__product__name_fr__icontains=value) \
                | Q(orderorderitems__product_card__product__name_ru__icontains=value) \
                | Q(orderorderitems__product_card__product__name_tm__icontains=value) \
                    | Q(orderorderitems__product_card__trade__name_fr__icontains=value) \
                        | Q(orderorderitems__product_card__lot__number__icontains=value) \
                        | Q(orderorderitems__product_card__lot__name_fr__icontains=value) \
                        | Q(orderorderitems__product_card__lot__name_ru__icontains=value) \
                            | Q(orderorderitems__product_card__annexe5__code__icontains=value) \
                            | Q(orderorderitems__product_card__annexe5__name_fr__icontains=value) \
                                | Q(orderorderitems__product_card__provider__code__icontains=value) \
                                | Q(orderorderitems__product_card__provider__name_fr__icontains=value)
        )


class AchatListView(generic.ListView):
    model = Order
    context_object_name = 'orders' 
    template_name = 'achat/achat.html'
    ordering = ['-created_at']
    paginate_by = 3

    def get_queryset(self):
        queryset = super(AchatListView, self).get_queryset()
        queryset = OrderCustomSearch(self.request.GET, queryset = queryset).qs
        
        return list(set(OrderFilter(self.request.GET, queryset=queryset).qs))


class OrderListView(generic.ListView):
    model = Order
    context_object_name = 'orders' 
    template_name = 'achat/orderlist.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        queryset = OrderCustomSearch(self.request.GET, queryset = queryset).qs
        return list(set(OrderFilter(self.request.GET, queryset=queryset).qs))

class OrderDetailView(generic.DeleteView):
    queryset = Order.objects.all()
    context_object_name = 'order' 
    template_name = 'achat/orderdetail.html'

