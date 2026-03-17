
from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import home, noticias


urlpatterns = [
    path('', views.home, name='home'),

    path('login/', RedirectView.as_view(pattern_name='plataforma_login'), name='login'),

    path('nosotros/', views.nosotros_view, name='nosotros'),
    path('historia/', views.historia_view, name='historia'),
    path('comunidad/', views.comunidad_view, name='comunidad'),

    path('noticias/', noticias, name='noticias'),

    path('admisiones/', views.admisiones_view, name='admisiones'),
    path('oferta-educativa/', views.oferta_educativa_view, name='oferta_educativa'),
    path('servicios-en-linea/', views.servicios_en_linea_view, name='servicios_en_linea'),
    path('utiles-escolares/', views.utiles_escolares_view, name='utiles-escolares'),
    path('ludicas/', views.ludicas_view, name='ludicas'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('panel/', views.panel_admin, name='panel_admin'),
    path('panel/toggle-user/<int:user_id>/', views.toggle_user, name='toggle_user'),
    path('panel/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    
]