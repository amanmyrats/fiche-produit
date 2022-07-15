from django.urls import path 
from django.contrib.auth import views as auth_views

  
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name = 'registration/login.html', success_url='home'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home.html', next_page='home'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html',success_url='/?passwordchanged=1'), name='password_change'),
]