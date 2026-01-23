from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import ContenidoInicio, GalleryImage
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def home(request):
    contenido = ContenidoInicio.objects.first()  # <- Aquí se añadió
    gallery_images = contenido.gallery_images.all() if contenido else []

    return render(request, 'core/home.html', {
        'contenido': contenido,
        'gallery_images': gallery_images,
    })

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

def nosotros_view(request):
    return render(request, 'core/nosotros.html')

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

def logout_view(request):
    logout(request)
    return redirect('home')

def panel_admin(request):
    return render(request, 'core/panel_admin.html')

def toggle_user(request, user_id):
    return redirect('panel_admin')

def delete_user(request, user_id):
    return redirect('panel_admin')

def gestionar_inicio(request):
    contenido, _ = ContenidoInicio.objects.get_or_create(pk=1)

    if request.method == 'POST':
        contenido.titulo_galeria = request.POST.get('titulo_galeria', '')
        contenido.url_manual = request.POST.get('url_manual', '')
        contenido.texto_direccion = request.POST.get('texto_direccion', '')
        contenido.iframe_mapa = request.POST.get('iframe_mapa', '')

        if 'logo' in request.FILES:
            contenido.logo = request.FILES['logo']
        if 'imagen_manual' in request.FILES:
            contenido.imagen_manual = request.FILES['imagen_manual']

        contenido.save()

        ordenes_usadas = set()

        for img in contenido.gallery_images.all():
            img_id = img.id
            img_field = f'imagen_{img_id}'
            desc_field = f'descripcion_{img_id}'
            orden_field = f'orden_{img_id}'
            delete_field = f'delete_{img_id}'

            if delete_field in request.POST:
                img.delete()
                continue

            if img_field in request.FILES:
                img.image = request.FILES[img_field]
            if desc_field in request.POST:
                img.descripcion = request.POST[desc_field]
            if orden_field in request.POST:
                try:
                    new_order = int(request.POST[orden_field])
                    if new_order != img.orden:
                        if GalleryImage.objects.filter(contenido=contenido, orden=new_order).exclude(pk=img.pk).exists():
                            messages.error(request, f"Orden duplicado: {new_order}")
                            continue
                        img.orden = new_order
                except ValueError:
                    messages.error(request, f"Orden inválido en imagen #{img_id}")
                    continue
            img.save()
            ordenes_usadas.add(img.orden)

        nuevas_imagenes = request.FILES.getlist('nuevas_imagenes')
        nuevas_descripciones = request.POST.get('nuevas_descripciones', '').splitlines()
        nuevas_ordenes = request.POST.get('nuevas_ordenes', '').splitlines()

        errores = []
        nuevas_ordenes_int = []

        for idx, orden_str in enumerate(nuevas_ordenes):
            try:
                orden_int = int(orden_str)
                if orden_int in ordenes_usadas or orden_int in nuevas_ordenes_int:
                    errores.append(f"Orden duplicado en nueva imagen #{idx + 1}: {orden_int}")
                else:
                    nuevas_ordenes_int.append(orden_int)
                    ordenes_usadas.add(orden_int)
            except ValueError:
                errores.append(f"Orden inválido en nueva imagen #{idx + 1}")

        if errores:
            for error in errores:
                messages.error(request, error)
            return redirect('gestionar_inicio')

        for imagen, descripcion, orden in zip(nuevas_imagenes, nuevas_descripciones, nuevas_ordenes_int):
            img = GalleryImage(
                contenido=contenido,
                image=imagen,
                descripcion=descripcion,
                orden=orden
            )
            try:
                img.save()
            except IntegrityError:
                messages.error(request, f"No se pudo guardar la imagen con orden {orden}.")
                continue

        messages.success(request, "Contenido de inicio actualizado correctamente.")
        return redirect('gestionar_inicio')

    context = {
        'contenido': contenido,
        'gallery_images': contenido.gallery_images.all(),
    }
    return render(request, 'core/gestionar_inicio.html', context)



# servicios en linea 

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
                fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
                hora = datetime.datetime.strptime(hora_str, '%H:%M').time()
            except (ValueError, TypeError):
                messages.error(request, 'Fecha u hora no válidas.')
                return redirect('gestionar_eventos')

            Evento.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                fecha=fecha,
                hora=hora,
                portada=portada,
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

    context = {'eventos': eventos}
    return render(request, 'core/gestionar_eventos.html', context)

def detalle_evento(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
        return render(request, 'core/detalle_evento.html', {'evento': evento})
    except Evento.DoesNotExist:
        messages.error(request, 'El evento solicitado no existe.')
        return redirect('home')
