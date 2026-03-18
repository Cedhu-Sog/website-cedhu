from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction, IntegrityError
from django.http import JsonResponse

from .models import Ludica, ProfesorLudica, EstudianteLudica, Inscripcion, GRADOS_CHOICES
from .decorators import admin_requerido, estudiante_ludica_requerido, profesor_ludica_requerido
from estudiantes.models import Estudiante


# =========================================================
# ADMIN — PANEL PRINCIPAL LÚDICAS
# =========================================================

@admin_requerido
def admin_dashboard_ludicas(request):
    """Panel central del admin para el módulo de lúdicas."""
    ludicas        = Ludica.objects.prefetch_related('inscripciones', 'profesor').all()
    total_ludicas  = ludicas.count()
    total_inscritos = Inscripcion.objects.filter(activa=True).count()
    total_profes   = ProfesorLudica.objects.filter(activo=True).count()
    total_estudiantes = EstudianteLudica.objects.filter(activo=True).count()

    context = {
        'ludicas': ludicas,
        'total_ludicas': total_ludicas,
        'total_inscritos': total_inscritos,
        'total_profes': total_profes,
        'total_estudiantes': total_estudiantes,
    }
    return render(request, 'ludicas/admin/dashboard.html', context)


# =========================================================
# ADMIN — GESTIÓN DE LÚDICAS (CRUD)
# =========================================================

@admin_requerido
def admin_lista_ludicas(request):
    ludicas = Ludica.objects.prefetch_related('inscripciones').select_related('profesor').all()
    return render(request, 'ludicas/admin/lista_ludicas.html', {
        'ludicas': ludicas,
        'grados_choices': GRADOS_CHOICES,
    })


@admin_requerido
def admin_crear_ludica(request):
    profesores = ProfesorLudica.objects.filter(activo=True)

    if request.method == 'POST':
        nombre      = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        profesor_id = request.POST.get('profesor')
        grados      = request.POST.getlist('grados_permitidos')
        cupo        = request.POST.get('cupo_maximo', 30)
        horario     = request.POST.get('horario', '').strip()
        lugar       = request.POST.get('lugar', '').strip()
        icono       = request.POST.get('icono', 'fa-star').strip()
        color       = request.POST.get('color', '#4f46e5').strip()
        estado      = request.POST.get('estado', 'ACTIVA')

        if not nombre:
            messages.error(request, 'El nombre de la lúdica es obligatorio.')
            return render(request, 'ludicas/admin/form_ludica.html', {
                'profesores': profesores,
                'grados_choices': GRADOS_CHOICES,
                'accion': 'Crear',
            })

        profesor = None
        if profesor_id:
            profesor = get_object_or_404(ProfesorLudica, id=profesor_id)

        Ludica.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            profesor=profesor,
            grados_permitidos=grados,
            cupo_maximo=int(cupo),
            horario=horario,
            lugar=lugar,
            icono=icono,
            color=color,
            estado=estado,
        )
        messages.success(request, f'Lúdica "{nombre}" creada exitosamente.')
        return redirect('admin_lista_ludicas')

    return render(request, 'ludicas/admin/form_ludica.html', {
        'profesores': profesores,
        'grados_choices': GRADOS_CHOICES,
        'accion': 'Crear',
    })


@admin_requerido
def admin_editar_ludica(request, ludica_id):
    ludica    = get_object_or_404(Ludica, id=ludica_id)
    profesores = ProfesorLudica.objects.filter(activo=True)

    if request.method == 'POST':
        ludica.nombre      = request.POST.get('nombre', ludica.nombre).strip()
        ludica.descripcion = request.POST.get('descripcion', '').strip()
        ludica.horario     = request.POST.get('horario', '').strip()
        ludica.lugar       = request.POST.get('lugar', '').strip()
        ludica.icono       = request.POST.get('icono', 'fa-star').strip()
        ludica.color       = request.POST.get('color', '#4f46e5').strip()
        ludica.estado      = request.POST.get('estado', 'ACTIVA')
        ludica.cupo_maximo = int(request.POST.get('cupo_maximo', ludica.cupo_maximo))
        ludica.grados_permitidos = request.POST.getlist('grados_permitidos')

        profesor_id = request.POST.get('profesor')
        ludica.profesor = get_object_or_404(ProfesorLudica, id=profesor_id) if profesor_id else None
        ludica.save()

        messages.success(request, f'Lúdica "{ludica.nombre}" actualizada.')
        return redirect('admin_lista_ludicas')

    return render(request, 'ludicas/admin/form_ludica.html', {
        'ludica': ludica,
        'profesores': profesores,
        'grados_choices': GRADOS_CHOICES,
        'accion': 'Editar',
    })


@admin_requerido
def admin_eliminar_ludica(request, ludica_id):
    ludica = get_object_or_404(Ludica, id=ludica_id)
    if request.method == 'POST':
        nombre = ludica.nombre
        ludica.delete()
        messages.success(request, f'Lúdica "{nombre}" eliminada.')
    return redirect('admin_lista_ludicas')


@admin_requerido
def admin_detalle_ludica(request, ludica_id):
    ludica = get_object_or_404(Ludica, id=ludica_id)
    inscripciones = ludica.inscripciones.filter(activa=True).select_related(
        'estudiante__estudiante'
    )
    return render(request, 'ludicas/admin/detalle_ludica.html', {
        'ludica': ludica,
        'inscripciones': inscripciones,
    })


# =========================================================
# ADMIN — GESTIÓN DE PROFESORES (CRUD)
# =========================================================

@admin_requerido
def admin_lista_profesores(request):
    profesores = ProfesorLudica.objects.prefetch_related('ludicas').all()
    return render(request, 'ludicas/admin/lista_profesores.html', {'profesores': profesores})


@admin_requerido
def admin_crear_profesor(request):
    if request.method == 'POST':
        nombres      = request.POST.get('nombres', '').strip()
        apellidos    = request.POST.get('apellidos', '').strip()
        documento    = request.POST.get('documento', '').strip()
        correo       = request.POST.get('correo', '').strip()
        telefono     = request.POST.get('telefono', '').strip()
        especialidad = request.POST.get('especialidad', '').strip()
        crear_usuario = request.POST.get('crear_usuario') == 'on'
        password     = request.POST.get('password', '').strip()

        if not all([nombres, apellidos, documento, correo]):
            messages.error(request, 'Nombres, apellidos, documento y correo son obligatorios.')
            return render(request, 'ludicas/admin/form_profesor.html', {'accion': 'Crear'})

        try:
            with transaction.atomic():
                user = None
                if crear_usuario and password:
                    username = f"prof_{documento}"
                    user = User.objects.create_user(
                        username=username,
                        email=correo,
                        password=password,
                        first_name=nombres,
                        last_name=apellidos,
                    )

                ProfesorLudica.objects.create(
                    nombres=nombres,
                    apellidos=apellidos,
                    documento=documento,
                    correo=correo,
                    telefono=telefono,
                    especialidad=especialidad,
                    user=user,
                )
            messages.success(request, f'Profesor {nombres} {apellidos} creado.')
            return redirect('admin_lista_profesores')
        except IntegrityError:
            messages.error(request, 'Ya existe un profesor con ese documento o correo.')

    return render(request, 'ludicas/admin/form_profesor.html', {'accion': 'Crear'})


@admin_requerido
def admin_editar_profesor(request, profesor_id):
    profesor = get_object_or_404(ProfesorLudica, id=profesor_id)

    if request.method == 'POST':
        profesor.nombres      = request.POST.get('nombres', profesor.nombres).strip()
        profesor.apellidos    = request.POST.get('apellidos', profesor.apellidos).strip()
        profesor.correo       = request.POST.get('correo', profesor.correo).strip()
        profesor.telefono     = request.POST.get('telefono', '').strip()
        profesor.especialidad = request.POST.get('especialidad', '').strip()
        profesor.activo       = request.POST.get('activo') == 'on'
        profesor.save()
        messages.success(request, 'Profesor actualizado.')
        return redirect('admin_lista_profesores')

    return render(request, 'ludicas/admin/form_profesor.html', {
        'profesor': profesor,
        'accion': 'Editar',
    })


@admin_requerido
def admin_eliminar_profesor(request, profesor_id):
    profesor = get_object_or_404(ProfesorLudica, id=profesor_id)
    if request.method == 'POST':
        nombre = str(profesor)
        profesor.delete()
        messages.success(request, f'Profesor {nombre} eliminado.')
    return redirect('admin_lista_profesores')


# =========================================================
# ADMIN — GESTIÓN DE ESTUDIANTES EN LÚDICAS (CRUD)
# =========================================================

@admin_requerido
def admin_lista_estudiantes_ludica(request):
    perfiles = EstudianteLudica.objects.select_related(
        'estudiante', 'estudiante__padre'
    ).prefetch_related('inscripciones__ludica').all()

    # Estudiantes del sistema que aún no tienen perfil lúdica
    ids_con_perfil = EstudianteLudica.objects.values_list('estudiante_id', flat=True)
    sin_perfil = Estudiante.objects.exclude(id__in=ids_con_perfil)

    return render(request, 'ludicas/admin/lista_estudiantes.html', {
        'perfiles': perfiles,
        'sin_perfil': sin_perfil,
    })


@admin_requerido
def admin_registrar_estudiante_ludica(request):
    """Crea perfil lúdica para un Estudiante existente."""
    ids_con_perfil = EstudianteLudica.objects.values_list('estudiante_id', flat=True)
    estudiantes_disponibles = Estudiante.objects.exclude(id__in=ids_con_perfil)

    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        crear_usuario = request.POST.get('crear_usuario') == 'on'
        password      = request.POST.get('password', '').strip()

        estudiante = get_object_or_404(Estudiante, id=estudiante_id)

        try:
            with transaction.atomic():
                user = None
                if crear_usuario and password:
                    username = f"est_{estudiante.documento}"
                    user = User.objects.create_user(
                        username=username,
                        email=estudiante.padre.correo,
                        password=password,
                        first_name=estudiante.nombres,
                        last_name=estudiante.apellidos,
                    )

                EstudianteLudica.objects.create(
                    estudiante=estudiante,
                    user=user,
                )
            messages.success(request, f'{estudiante.nombres} registrado en lúdicas.')
            return redirect('admin_lista_estudiantes_ludica')
        except IntegrityError:
            messages.error(request, 'Error al registrar el estudiante.')

    return render(request, 'ludicas/admin/form_estudiante_ludica.html', {
        'estudiantes_disponibles': estudiantes_disponibles,
    })


@admin_requerido
def admin_toggle_estudiante_ludica(request, perfil_id):
    perfil = get_object_or_404(EstudianteLudica, id=perfil_id)
    if request.method == 'POST':
        perfil.activo = not perfil.activo
        perfil.save()
        estado = 'activado' if perfil.activo else 'desactivado'
        messages.success(request, f'{perfil.nombre_completo} {estado}.')
    return redirect('admin_lista_estudiantes_ludica')


@admin_requerido
def admin_eliminar_estudiante_ludica(request, perfil_id):
    perfil = get_object_or_404(EstudianteLudica, id=perfil_id)
    if request.method == 'POST':
        nombre = perfil.nombre_completo
        # Eliminar user asociado si existe
        if perfil.user:
            perfil.user.delete()
        else:
            perfil.delete()
        messages.success(request, f'Perfil de {nombre} eliminado.')
    return redirect('admin_lista_estudiantes_ludica')


# =========================================================
# ADMIN — INSCRIPCIONES
# =========================================================

@admin_requerido
def admin_inscribir_estudiante(request, perfil_id):
    """El admin puede inscribir manualmente a un estudiante en una lúdica."""
    perfil  = get_object_or_404(EstudianteLudica, id=perfil_id)
    grado   = perfil.grado
    ludicas = Ludica.objects.filter(
        estado__in=['ACTIVA', 'COMPLETA'],
        grados_permitidos__contains=grado,
    )

    if request.method == 'POST':
        ludica_id = request.POST.get('ludica_id')
        ludica    = get_object_or_404(Ludica, id=ludica_id)

        # Cancelar inscripción anterior si existe
        Inscripcion.objects.filter(estudiante=perfil, activa=True).update(activa=False)

        try:
            Inscripcion.objects.create(estudiante=perfil, ludica=ludica, activa=True)
            messages.success(request, f'{perfil.nombre_completo} inscrito en "{ludica.nombre}".')
        except ValueError as e:
            messages.error(request, str(e))
        except IntegrityError:
            # Ya existía, reactivar
            insc = Inscripcion.objects.get(estudiante=perfil, ludica=ludica)
            insc.activa = True
            insc.save()
            messages.success(request, f'Inscripción reactivada en "{ludica.nombre}".')

        return redirect('admin_lista_estudiantes_ludica')

    return render(request, 'ludicas/admin/inscribir_estudiante.html', {
        'perfil': perfil,
        'ludicas': ludicas,
    })


@admin_requerido
def admin_cancelar_inscripcion(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    if request.method == 'POST':
        inscripcion.activa = False
        inscripcion.save()
        # Liberar cupo: si la lúdica estaba COMPLETA, volver a ACTIVA
        ludica = inscripcion.ludica
        if ludica.estado == 'COMPLETA' and not ludica.esta_llena:
            ludica.estado = 'ACTIVA'
            ludica.save(update_fields=['estado'])
        messages.success(request, 'Inscripción cancelada.')
    return redirect('admin_lista_estudiantes_ludica')


# =========================================================
# ESTUDIANTE — DASHBOARD DE LÚDICAS
# =========================================================

@estudiante_ludica_requerido
def estudiante_dashboard(request):
    perfil         = request.user.estudiante_ludica
    inscripcion    = perfil.inscripcion_activa
    grado          = perfil.grado

    # Lúdicas disponibles para su grado
    todas_ludicas  = Ludica.objects.filter(
        estado__in=['ACTIVA', 'COMPLETA'],
    ).select_related('profesor').prefetch_related('inscripciones')

    ludicas_grado = [l for l in todas_ludicas if grado in l.grados_permitidos]

    context = {
        'perfil': perfil,
        'inscripcion': inscripcion,
        'ludicas_grado': ludicas_grado,
    }
    return render(request, 'ludicas/estudiante/dashboard.html', context)


@estudiante_ludica_requerido
def estudiante_escoger_ludica(request, ludica_id):
    perfil = request.user.estudiante_ludica
    ludica = get_object_or_404(Ludica, id=ludica_id)

    if request.method == 'POST':
        # Cancelar inscripción actual
        Inscripcion.objects.filter(estudiante=perfil, activa=True).update(activa=False)

        try:
            # Intentar crear o reactivar
            insc, created = Inscripcion.objects.get_or_create(
                estudiante=perfil,
                ludica=ludica,
                defaults={'activa': True},
            )
            if not created:
                insc.activa = True
                insc.save()
            messages.success(request, f'¡Te inscribiste en "{ludica.nombre}"!')
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('estudiante_dashboard_ludicas')

    return render(request, 'ludicas/estudiante/confirmar_inscripcion.html', {
        'perfil': perfil,
        'ludica': ludica,
    })


@estudiante_ludica_requerido
def estudiante_cancelar_inscripcion(request):
    perfil = request.user.estudiante_ludica
    if request.method == 'POST':
        insc = perfil.inscripcion_activa
        if insc:
            ludica = insc.ludica
            insc.activa = False
            insc.save()
            if ludica.estado == 'COMPLETA' and not ludica.esta_llena:
                ludica.estado = 'ACTIVA'
                ludica.save(update_fields=['estado'])
            messages.success(request, 'Has cancelado tu inscripción.')
        else:
            messages.warning(request, 'No tienes una inscripción activa.')
    return redirect('estudiante_dashboard_ludicas')