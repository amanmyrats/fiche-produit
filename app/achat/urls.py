from django.urls import path

from achat.views import order_create_view, AchatListView, OrderListView, OrderDetailView, order_edit_view


urlpatterns = [

    path('', AchatListView.as_view(), name='achat'),
    path('orders/', OrderListView.as_view(), name = 'orderlist'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name = 'orderdetail'),
    path('orders/create/', order_create_view, name = 'ordercreate'),
    path('orders/<int:pk>/edit/', order_edit_view, name = 'orderedit'),

]
