"""
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import FPViewSet, ProductViewSet, ProductViewSet, OrderViewSet, FactureViewSet, \
    SpecificationViewSet, DeclarationViewSet, TdsViewSet, CooViewSet, RoutageViewSet #  FPListCreateAPIView, FPRetrieveAPIView, ProductListCreateAPIView, ProductRetrieveAPIView, ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'fps', FPViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'factures', FactureViewSet)
router.register(r'specifications', SpecificationViewSet)
router.register(r'tds', TdsViewSet)
router.register(r'declarations', DeclarationViewSet)
router.register(r'coo', CooViewSet)
router.register(r'routages', RoutageViewSet)
# router.register(r'tests', ServiceAchatView)



urlpatterns = [
    # path('api/fps/', FPListCreateAPIView.as_view(), name='api-fps'),
    # path('api/fps/<int:pk>/', FPRetrieveAPIView.as_view(), name='api-fps-detail'),
    path(r'api/', include(router.urls)),
]