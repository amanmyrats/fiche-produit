import json

from django.shortcuts import render

from fiche_produit.models import Project, FactureItem, SpecificationItem, DeclarationItem, TdsItem


def qs_view(request):
    # ['Annexe', 'Order', 'Facture', 'TDS', 'Declaration', 'Paid']
    cra = Project.objects.get(id=1)
    annexe_items = cra.annexe5_set.all()
    orders = cra.order_set.all()
    factures = cra.facture_set.all()
    # print('factures:', factures)
    facture_items_for_tds_and_declaration = FactureItem.objects.filter(facture__in = factures)
    # print('facture items:', facture_items_for_tds_and_declaration)
    tdss = TdsItem.objects.filter(facture_item__in = facture_items_for_tds_and_declaration)
    # print('tdss:',tdss )
    declarations = DeclarationItem.objects.filter(facture_item__in = facture_items_for_tds_and_declaration)
    # print('declarations:', declarations)
    annexe_total = 0
    order_total = 0
    facture_total = 0
    tds_total = 0
    declaration_total = 0
    paid_total = 0


    for annexe_item in annexe_items:
        try:
            annexe_total += annexe_item.total_price
        except:
            pass
    
    for order in orders:
        try:
            order_total += order.total_sum
        except:
            pass
    
    for facture in factures:
        try:
            facture_total += facture.total_sum
        except:
            pass
    
    for tds in tdss:
        try:
            tds_total += tds.facture_item.total_price
        except:
            pass

    for declaration in declarations:
        try:
            declaration_total += declaration.facture_item.total_price
        except:
            pass

    data = [float(annexe_total),float(order_total),float(facture_total),float(tds_total), float(declaration_total), float(paid_total)]  
    context = {
        'project':cra,
        'data':data
    }
    return render(request, 'qs/qs.html', context)
