from binascii import a2b_qp
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from django.conf.urls.i18n import i18n_patterns

from django.conf import settings
from django.conf.urls.static import static


from fiche_produit.views import home_view, export_view, test_view
from achat.views import achat_view, order_create_view, AchatListView, OrderListView, OrderDetailView, order_edit_view
from logistics.views import logistics_view, LogisticsListView, facture_create_view, FactureListView, FactureDetailView, facture_edit_view


urlpatterns = i18n_patterns(
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),  # NEW
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name = 'registration/login.html', success_url='home'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home.html', next_page='home'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html',success_url='/?passwordchanged=1'), name='password_change'),
    
    path('site/', include('fiche_produit.urls')),
    path('chantier/', include('chantier.urls')),
    path('achat/', include('achat.urls')),
    path('logistics/', include('logistics.urls')),
    path('qs/', include('qs.urls')),

    path('api/', include('api.urls')),

    path('export/', export_view, name='export'),
    path('test/', test_view, name='test'),
) 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

