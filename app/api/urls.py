from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import FPViewSet, ProductViewSet, ProductViewSet, OrderViewSet, FactureViewSet, \
    SpecificationViewSet, DeclarationViewSet, TdsViewSet, CooViewSet, RoutageViewSet, \
        OrderItemViewSet, FactureItemViewSet, ProductCardAnnexe5ViewSet, \
            fp_number_generator


app_name = 'api'

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'fps', FPViewSet, basename='fps')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'orderitems', OrderItemViewSet, basename='orderitems')
router.register(r'factures', FactureViewSet, basename='factures')
router.register(r'factureitems', FactureItemViewSet, basename='factureitems')
router.register(r'specifications', SpecificationViewSet, basename='specifications')
router.register(r'tds', TdsViewSet)
router.register(r'declarations', DeclarationViewSet, basename='declarations')
router.register(r'coo', CooViewSet)
router.register(r'routages', RoutageViewSet, basename='routages')
router.register(r'fpannexe5', ProductCardAnnexe5ViewSet)
# router.register(r'tests', ServiceAchatView)



urlpatterns = [
    path(r'', include(router.urls)),
    path(r'newnumber/', fp_number_generator, name='fp-number-generator')
]