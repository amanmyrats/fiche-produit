from django.contrib import admin

from fiche_produit.models import *

# Register your models here.


admin.site.register(Product)
admin.site.register(Lot)
admin.site.register(Project)
admin.site.register(Provider)
admin.site.register(Country)
admin.site.register(Room)
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(ProductCard)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Facture)
admin.site.register(FactureItem)
admin.site.register(Specification)
admin.site.register(SpecificationItem)
admin.site.register(Tds)
admin.site.register(TdsItem)
admin.site.register(Declaration)
admin.site.register(DeclarationItem)
admin.site.register(Coo)
admin.site.register(CooFacture)

