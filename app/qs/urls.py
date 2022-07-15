from django.urls import path

from qs.views import qs_view


urlpatterns = [
    path('', qs_view, name='qs'),
]