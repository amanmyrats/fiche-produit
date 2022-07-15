from os import stat
from django.http import response
import requests

from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from rest_framework  import status
import django_filters
from django.db.models import Q

from .forms import   FactureItemModelForm, FactureModelForm
from fiche_produit.models import Facture



mysitedomain = 'http://127.0.0.1:8000/'



def logistics_view(request):
    factures = Facture.objects.all()
    context = {
        'factures':factures
    }
    return render(request, 'logistics/logistics.html', context)


def facture_create_view(request):
    factureform = FactureModelForm
    if request.method=='POST':
        factureform = FactureModelForm(request.POST)
        # url = mysitedomain + 'api/factures/'
        data = request.POST
        # print('data to be sent:', data)
        facture_create_request = requests.post(url=request.build_absolute_uri(reverse('api:factures-list')), data = data)
        response =facture_create_request.json()
        if status.is_success(facture_create_request.status_code):
            # print('response:', response)
            new_facture_id = response.get('id')
            # print('facture response', response)
            # print('new id', new_facture_id)
            return redirect(reverse('factureedit', kwargs={'pk':new_facture_id}))
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
        # print('item_id', item_id)
        item = facture.factureitems.get(pk = item_id)
        factureitemform = FactureItemModelForm(instance=item)
        buttonname = 'Save Edit'
        show_form = True
    elif request.GET.get('additem'):
        factureitemform = FactureItemModelForm
        show_form = True
        

    if request.method=='POST':
        factureitemform = FactureItemModelForm(request.POST)
        # url_add = mysitedomain + 'api/factureitems/'
        # url_patch = mysitedomain + 'api/factureitems/{}/'.format(item_id)
        data = request.POST.copy()
        data['facture']=facture_id

        if request.GET.get('additem'):
            facture_add_item_request = requests.post(url = request.build_absolute_uri(reverse('api:factureitems-list')), data=data)
        elif request.GET.get('edititem'):
            facture_add_item_request = requests.patch(url = request.build_absolute_uri(reverse('api:factureitems-detail', kwargs={'pk':item_id})), data=data)

        # print('facture_add_item_request response', facture_add_item_request)
        if status.is_success(facture_add_item_request.status_code):
            return redirect(reverse('factureedit', kwargs={'pk':facture_id}))


    context = {
        'facture':facture,
        'existing_items':existing_items,
        'factureitemform':factureitemform,
        'buttonname':buttonname,
        'show_form':show_form
    }
    return render(request, 'logistics/factureitemform.html', context)


class FactureFilter(django_filters.FilterSet):
    trade = django_filters.CharFilter(field_name = 'factureitems__order_item__product_card__trade')
    lot = django_filters.CharFilter(field_name = 'factureitems__order_item__product_card__lot')
    annexe5 = django_filters.CharFilter(field_name = 'factureitems__order_item__product_card__annexe5')
    provider  = django_filters.CharFilter(field_name = 'factureitems__order_item__product_card__provider')
    
    class Meta:
        model = Facture
        fields = ['project']


class FactureCustomSearch(django_filters.FilterSet):
    search = django_filters.CharFilter(method = 'search_everywhere', label='Search')

    class Meta:
        model = Facture
        fields = ['search']
    
    def search_everywhere(self, queryset, name, value):
        return Facture.objects.filter(
            # Q(location__name_tm__icontains=value)
            Q(project__code__icontains=value) | Q(number__icontains=value) \
                | Q(factureitems__order_item__product_card__product__name_en__icontains=value) \
                | Q(factureitems__order_item__product_card__product__name_fr__icontains=value) \
                | Q(factureitems__order_item__product_card__product__name_ru__icontains=value) \
                | Q(factureitems__order_item__product_card__product__name_tm__icontains=value) \
                    | Q(factureitems__order_item__product_card__trade__name_fr__icontains=value) \
                        | Q(factureitems__order_item__product_card__lot__number__icontains=value) \
                        | Q(factureitems__order_item__product_card__lot__name_fr__icontains=value) \
                        | Q(factureitems__order_item__product_card__lot__name_ru__icontains=value) \
                            | Q(factureitems__order_item__product_card__annexe5__code__icontains=value) \
                            | Q(factureitems__order_item__product_card__annexe5__name_fr__icontains=value) \
                                | Q(factureitems__order_item__product_card__provider__code__icontains=value) \
                                | Q(factureitems__order_item__product_card__provider__name_fr__icontains=value)
        )


class LogisticsListView(generic.ListView):
    model = Facture
    context_object_name = 'factures' 
    template_name = 'logistics/logistics.html'
    ordering = ['-date']
    paginate_by = 3

    def get_queryset(self):
        queryset = super(LogisticsListView, self).get_queryset()
        queryset = FactureCustomSearch(self.request.GET, queryset = queryset).qs
        
        return list(set(FactureFilter(self.request.GET, queryset=queryset).qs))


class FactureListView(generic.ListView):
    model = Facture
    context_object_name = 'factures' 
    template_name = 'logistics/facturelist.html'
    ordering = ['-date']
    paginate_by = 3

    def get_queryset(self):
        queryset = super(FactureListView, self).get_queryset()
        queryset = FactureCustomSearch(self.request.GET, queryset = queryset).qs
        return list(set(FactureFilter(self.request.GET, queryset=queryset).qs))

class FactureDetailView(generic.DeleteView):
    queryset = Facture.objects.all()
    context_object_name = 'facture' 
    template_name = 'logistics/facturedetail.html'
