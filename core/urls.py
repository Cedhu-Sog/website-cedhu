from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),

    path('nosotros/', views.nosotros_view, name='nosotros'),
    path('historia/', views.historia_view, name='historia'),
    path('admisiones/', views.admisiones_view, name='admisiones'),
    path('oferta-educativa/', views.oferta_educativa_view, name='oferta_educativa'),
    path('servicios-en-linea/', views.servicios_en_linea_view, name='servicios_en_linea'),
    path('utiles-escolares/', views.utiles_escolares_view, name='utiles-escolares'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('logout/', views.logout_view, name='logout'),

    path('panel/', views.panel_admin, name='panel_admin'),
    path('panel/toggle-user/<int:user_id>/', views.toggle_user, name='toggle_user'),
    path('panel/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('panel/gestionar-inicio/', views.gestionar_inicio, name='gestionar_inicio'),
]






