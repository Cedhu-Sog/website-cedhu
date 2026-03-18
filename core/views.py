# views.py

from django.shortcuts import render, redirect
import logging
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import datetime

from .models import ContenidoInicio, GalleryImage, Noticia, Evento
from plataforma.models import Staff

logger = logging.getLogger(__name__)


# ==============================
# HOME
# ==============================

def home(request):
    contenido = ContenidoInicio.objects.first()

    gallery_images = []
    if contenido:
        gallery_images = contenido.gallery_images.all()

    noticias_home = Noticia.objects.filter(activa=True)
    eventos = Evento.objects.all()

    return render(request, "core/home.html", {
        "contenido": contenido,
        "gallery_images": gallery_images,
        "noticias_home": noticias_home,
        "eventos": eventos
    })


# ==============================
# LOGIN / LOGOUT
# ==============================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('panel_admin')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ==============================
# PÁGINAS
# ==============================

def nosotros_view(request):
    staff_qs = Staff.objects.all().order_by('nombre')
    grouped = {key: [] for key, _ in Staff.CATEGORIAS}
    extras = {}

    for persona in staff_qs:
        if persona.categoria in grouped:
            grouped[persona.categoria].append(persona)
        else:
            extras.setdefault(persona.categoria, []).append(persona)

    counts = {key: len(items) for key, items in grouped.items()}
    logger.info("Staff counts (core.nosotros_view): %s", counts)
    if extras:
        extras_counts = {key: len(items) for key, items in extras.items()}
        logger.warning("Staff con categorias invalidas: %s", extras_counts)

    return render(request, 'core/nosotros.html', {
        'directivas': grouped.get('directivas', []),
        'coordinadores': grouped.get('coordinadores', []),
        'docentes': grouped.get('docentes', []),
        'administrativos': grouped.get('administrativos', []),
        'servicios': grouped.get('servicios', []),
    })


def historia_view(request):
    return render(request, 'core/historia.html')


def comunidad_view(request):
    return render(request, 'core/comunidad.html')


def admisiones_view(request):
    return render(request, 'core/admisiones.html')


def oferta_educativa_view(request):
    return render(request, 'core/oferta_educativa.html')


def servicios_en_linea_view(request):
    return render(request, 'core/servicios_en_linea.html')


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def utiles_escolares_view(request):
    return render(request, 'core/utiles_escolares.html')


def ludicas_view(request):
    return render(request, 'core/ludicas.html')


def noticias(request):
    noticias = Noticia.objects.filter(activa=True)

    return render(request, 'core/noticias.html', {
        'noticias': noticias
    })


# ==============================
# PANEL ADMIN
# ==============================

def panel_admin(request):
    return render(request, 'core/panel_admin.html')


def toggle_user(request, user_id):
    return redirect('panel_admin')


def delete_user(request, user_id):
    return redirect('panel_admin')



# ==============================
# EVENTOS
# ==============================

@login_required
def gestionar_eventos(request):

    eventos = Evento.objects.all().order_by('-fecha')

    if request.method == 'POST':

        if 'crear_evento' in request.POST:

            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            fecha_str = request.POST.get('fecha')
            hora_str = request.POST.get('hora')
            portada = request.FILES.get('portada')

            try:

                fecha = datetime.datetime.strptime(
                    fecha_str,
                    '%Y-%m-%d'
                ).date()

                hora = datetime.datetime.strptime(
                    hora_str,
                    '%H:%M'
                ).time()

            except (ValueError, TypeError):

                messages.error(request, 'Fecha u hora no válidas.')
                return redirect('gestionar_eventos')

            Evento.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                fecha=fecha,
                hora=hora,
                portada=portada
            )

            messages.success(request, 'Evento creado exitosamente.')

        elif 'eliminar_evento' in request.POST:

            evento_id = request.POST.get('evento_id')

            try:

                evento = Evento.objects.get(id=evento_id)
                evento.delete()

                messages.success(request, 'Evento eliminado correctamente.')

            except Evento.DoesNotExist:

                messages.error(request, 'El evento no existe.')

        return redirect('gestionar_eventos')

    context = {
        'eventos': eventos
    }

    return render(request, 'core/gestionar_eventos.html', context)


def detalle_evento(request, evento_id):

    try:

        evento = Evento.objects.get(id=evento_id)

        return render(request, 'core/detalle_evento.html', {
            'evento': evento
        })

    except Evento.DoesNotExist:

        messages.error(request, 'El evento solicitado no existe.')

        return redirect('home')
