
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator

from django.core.files.storage import FileSystemStorage
from pathlib import Path
from os import remove, path

BASE_DIR = Path(__file__).resolve().parent.parent
from .crys import *


def loginFormulario(request):
    """Esta funcion renderiza el formulacio de login.

    Returns:
        html:Pagina de login.
    """
    return render(request, 'login/login.html')


def login(request):
    """"Esta funcion valida el logueo de un
    usuario,  crea una variable de sesion.

    Args:
        user (str): Nombre de usuario.
        pasw (str): Password de usuario.

    Returns:
        html:Pagina de inicio.
    """
    if request.method == "POST":
        try:
            # capturar datos del formulario
            user = request.POST["usua"]
            pasw = claveEncriptada(request.POST['clave'])

            print(f'{user}-{pasw} -------------')
            # verificar si existe en base de datos
            q = Usuarios.objects.get(usuario=user, contraseña=pasw)

            # crear la variable de sesion
            request.session["logueo"] = [q.id, q.nombre, q.apellido, q.rol, q.get_rol_display()]
            messages.success(request, 'bienvenido')
            return redirect('checho:index')
        except Usuarios.DoesNotExist:
            messages.error(request, "Usuario o contraseña incorrectos...")
            return redirect('checho:loginFormulario')
    else:
        return redirect('checho:loginFormulario')


def logout(request):
    """"Esta funcion cierra la sesion de un usuario
    y elimina la variable de sesion.

    Returns:
        html: Pagina de inicio.
    """
    try:
        del request.session["logueo"]
        messages.success(request, "Sesión cerrada correctamente!")
    except Exception as e:
        messages.error(request, "Ocurrió un error, intente de nuevo...")

    return redirect('checho:index')


# return HttpResponseRedirect(reverse('territorio:aprendiz'))

#
def index(request):
    """Esta funcion renderiza
    la pagina de inicio.

    Returns:
        html: Pagina de inicio.
    """
    return render(request, 'index.html')


# Crud usuarios
def listarUsuarios(request):
    """Esta funcion consulta   una lista
    de usuarios de la base de datos.

    Returns:
        html: Listado de usuarios.
    """
    login = request.session.get('logueo', False)
    if login and login[4] == 'Administrador':
        q = Usuarios.objects.all()
        pag = Paginator(q, 5)  # cinco registros por página
        page_number = request.GET.get('page')

        # sobreescribo el query
        q = pag.get_page(page_number)

        contexto = {'page_obj': q}
        return render(request, 'usuario/listarUsuario.html', contexto)

    elif login and login[4] != 'Administrador':
        messages.info(request, 'No tiene permisos para ver este modulo')
        return redirect('checho:index')

    else:
        messages.warning(request, 'No esta logueado')
        return redirect('checho:login')


def eliminarUser(request, id):
    """Esta funcion consulta un usuario en la
    base de datos por id y lo elimina.

    Args:
        id (int): Recibe el id del usuario.

    Returns:
        html: pagina donde se listan los usuario.
    """
    try:
        q = Usuarios.objects.get(id=id)

        q.delete()
        messages.success(request, 'Usuario Eliminado')
        return redirect('checho:listarUsuarios')
    except Exception as e:
        return HttpResponse(f'  {e}')


def registrarUsuario(request):
    """Esta funcion renderiza la pagina para
    realizar los registros de los usuarios.

    Returns:
        html: Pagina para registro de usuarios
    """

    return render(request, 'usuario/registrarUsuario.html')


def guardarUsuario(request):
    """Esta funcion recibe los parametros enviados
     por post y crea un usuario en la base de datos.

     Args:
        f (file): Foto del usuario
        nom (str): Nombre del usuario
        apell (str): Apellidoo del usuario
        numTel (int): Numero de telefono del usuario
        correo (str): Correo del usuario
        palabraClave (str): Palabra de seguridad
        user (str): Usuario
        contra (str): Password

     Returns:
           html: Pagina de inicio
    """
    try:
        if request.method == 'POST':

            if request.FILES:
                # Crear instancia de File System Storage
                fss = FileSystemStorage()
                # Capturar la foto del formulario
                f = request.FILES["foto"]
                # Cargar archivo al servidor
                file = fss.save("checho/fotos/" + f.name, f)
                print('-------------------- pailas -----')

            else:

                file = "checho/fotos/default.png"

            nom = request.POST['nombre']
            apell = request.POST['apellido']
            numTel = request.POST['telefono']
            correo = request.POST['correo']
            palabraC = request.POST['palabraClave']
            user = request.POST['user']
            contra = claveEncriptada(request.POST['passw'])

            q = Usuarios.objects.create(nombre=nom, apellido=apell, numeroTelefono=numTel,
                                        correo=correo, palabraClave=palabraC, usuario=user,
                                        contraseña=contra, foto=file)

            messages.success(request, 'Usuario agregado')

            return redirect('checho:login')

        else:

            messages.warning(request, "Usted no envio datos ")
            return redirect('checho:index')
    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('checho:index')



def editarUsuarios(request, id):
    """Esta funcion consulta  un usuario
    en la base de datos por id.

    Args:
        id (int): Recibe el id del usuario.

    Returns:
        html: Pagina del formulario para editar el usuario.
    """

    login = request.session.get('logueo', False)
    if login and login[4] == 'Administrador':
        usuario = Usuarios.objects.get(id=id)
        return render(request, 'usuario/usuarioEditar.html', {'usuario': usuario})

    elif login and login[4] != 'Administrador':
        messages.info(request, 'No tienes permiso para editar al usuario')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Tiene que iniciar sesión')
        return redirect('checho:login')


def guardadoUsuario(request):
    """Esta funcion consulta un usuario
     en la base de datos por id y
     actualiza sus datos.

     Args:
         nom (str): Nombre del usuario
         ape (str): Apellido del usuario
         tel (int): Telefono del usuario
         id (int): Id del usuario
         rol (str): Rol del usuario

     Returns:
         html: Pagina para listar los usuarios.
    """
    try:
        if request.method == 'POST':
            nom = request.POST['nombre']
            ape = request.POST['apellido']
            tel = request.POST['telefono']
            id = request.POST['id']
            rol = request.POST['rol']

            usuarios = Usuarios.objects.get(id=id)

            usuarios.nombre = nom
            usuarios.apellido = ape
            usuarios.numeroTelefono = tel
            usuarios.rol = rol

            usuarios.save()

            messages.success(request, 'Usuario agregado')

            return redirect('checho:listarUsuarios')

        else:

            messages.warning(request, "Usted no envio datos ")
            return redirect('checho:listarUsuarios')

    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('checho:listarUsuarios')


# Actualizacion del perfil del usuario
def perfil(request):
    """Esta funcion renderiza el perfil del usuario.

    Returns:
        html: Formulario para editar el perfil del usuario.
    """
    login = request.session.get('logueo', False)
    if login:
        q = Usuarios.objects.get(pk=login[0])
        contexto = {'perfil': q}
        return render(request, 'usuario/perfil.html', contexto)
    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:login')


def actualizarPerfil(request):
    """Esta funcion consulta un usuario por id
    en la base de datos y actualiza su perfil.


    Args:
        q.nombre (str): Nombre de usuario
        q.apellido (str): Apellido de usuario
        q.numeroTelefono (str): Numero de telefono del usuario
        q.contraseña (str): Password del usuario

    Returns:
          html: Pefil del usuario

    """
    if request.method == "POST":
        try:
            login = request.session.get('logueo', False)
            q = Usuarios.objects.get(pk=login[0])
            q.nombre = request.POST["nombre"]
            q.apellido = request.POST["apellido"]
            q.numeroTelefono = request.POST["telefono"]
            # Cambio para los datos unicos de la base de datos
            if q.usuario != request.POST["usuario"]:
                try:
                    consulta = Usuarios.objects.get(usuario=request.POST["usuario"])
                    raise Exception("Usuario ya existe....")
                except Usuarios.DoesNotExist:
                    q.usuario = request.POST["usuario"]

            else:
                q.usuario = request.POST["usuario"]

            if request.POST["password"] != "":
                q.contraseña = claveEncriptada(request.POST["password"])

            q.save()

            # Cambiar datos de la sesion
            login[1] = q.nombre
            login[2] = q.apellido
            request.session["logueo"] = login

            messages.success(request, "Perfil actualizado correctamente!")
        except Usuarios.DoesNotExist:
            messages.error(request, "No existe el usuario...")
        except Exception as e:
            messages.error(request, f'Error: {e}')
    else:
        messages.warning(request, "No envió datos...")

    return redirect('checho:perfil')

#ver cita del usuario
def verMiCita(request):
    login = request.session.get('logueo', False)
    if login and login[4] == 'Cliente':
        try:

            login = request.session.get('logueo', False)
            u = Usuarios.objects.get(pk=login[0])
            citas = Citas.objects.filter(usuarioCliente=u.id)
            pag = Paginator(citas, 5)
            page_number = request.GET.get('page')
            citas = pag.get_page(page_number)
            contexto = {'page_obj': citas}
            return render(request, 'usuario/vercitas.html', contexto)

        except Exception as e:
            messages.error(request,e)
            return  redirect('checho:index')

    elif login and login[4] != 'Cliente':
        messages.warning(request, 'No tiene permisos para acceder a esta url')
        return redirect('checho:index')

    else:
        messages.info(request, 'Debe iniciar sesión')
        return redirect('checho:index')

def verAgendaEmpleado(request):
    login = request.session.get('logueo', False)
    if login and login[4] == 'Empleado':
        try:

            u = Usuarios.objects.get(pk=login[0])

            citas = Citas.objects.filter(usuarioEmpleado=u.id)
            pag = Paginator(citas, 5)
            page_number = request.GET.get('page')
            citas = pag.get_page(page_number)
            contexto = {'page_obj': citas}
            return render(request, 'usuario/verAgendaEmpleado.html', contexto)

        except Exception as e:
            messages.error(request,e)
            return  redirect('checho:index')

    elif login and login[4] != 'Empleado':
        messages.warning(request, 'No tiene permisos para acceder a esta url')
        return redirect('checho:index')
    else:
        messages.info(request, 'Debe iniciar sesión')
        return redirect('checho:index')

# Crud servicios
def servicios(request):
    """Esta funcion consulta los servicios en la base de datos.

    Returns:
        html: Pagina para listar los servicios.
    """

    login = request.session.get('logueo', False)
    if login and (login[4] == 'Administrador' or login[4] == 'Empleado'):
        q = Servicios.objects.all()
        pag = Paginator(q, 5)  # cinco registros por página
        page_number = request.GET.get('page')

        # sobreescribo el query
        q = pag.get_page(page_number)

        contexto = {'page_obj': q}
        return render(request, 'servicios/listarServicios.html', contexto)

    elif login and (login[4] != 'Administrador' or login[4] != 'Empleado'):
        messages.info(request, 'No tienes permisos para ingresar a este módulo')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debes iniciar sesión')
        return redirect('checho:login')


def registrarServicio(request):
    """Esta funcion renderiza la pagina de registro de servicio.

    Returns:
        html: Pagina del formulario para registrar un servicio.
    """
    login = request.session.get('logueo', False)
    if login and (login[4] == 'Administrador' or login[4] == 'Empleado'):
        return render(request, 'servicios/registrarServicios.html')

    elif login and (login[4] != 'Administrador' or login[4] != 'Empleado'):
        messages.info(request, 'No tienes permisos para ingresar a este módulo')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debes iniciar sesión')
        return redirect('checho:login')


def guardarServicio(request):
    """Esta funcion recibe datos por el metodo
    post y crea un servicio.

    Args:
        foto (file): Foto del servicio
        nomSer (str): Nombre del servicio
        precio (int): Precio del servicio
        descripcion (str): Descripcion del servicio
        categoria (str): Categoria del servicio

    Returns:
        html: Pagina donde se listan los servicios.
    """
    try:
        if request.method == 'POST':

            if request.FILES:
                # Crear instancia de File System Storage
                fss = FileSystemStorage()
                # Capturar la foto del formulario
                f = request.FILES["foto"]
                # Cargar archivo al servidor
                file = fss.save("checho/fotos/" + f.name, f)
                print('-------------------- pailas -----')

            else:

                file = "checho/fotos/default.png"

            nomSer = request.POST['nombre']
            precio = request.POST['precio']
            descripcion = request.POST['descripcion']
            categoria = request.POST['categoria']

            q = Servicios.objects.create(nombreServicio=nomSer, precio=precio, descripcion=descripcion, categoria=categoria,
                                        foto=file)

            messages.success(request, 'Servicio agregado')

            return redirect('checho:listarServicios')

        else:

            messages.warning(request, "Usted no envio datos ")
            return redirect('checho:listarServicios')
    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('checho:listarServicios')


def eliminarServicio(request, id):
    """Esta funcion elimina un servicio de la
    base de datos por id.

    Args:
        id (int): Id del servicio.

    Returns:
        html: Listado de servicios.
    """
    try:
        q = Servicios.objects.get(id=id)

        q.delete()
        messages.success(request, 'Servicio Eliminado')
        return redirect('checho:listarServicios')
    except Exception as e:
        return HttpResponse(f'  {e}')


def editarServicio(request, id):
    """Esta funcion consulta un servicio por id
    y lo envia como parametro.

    Args:
        id (int): id de servicio.

    Returns:

          html: Pagina de editar servicios.
    """

    login = request.session.get('logueo', False)

    if login and (login[4] == 'Administrador' or login[4] == 'Empleado'):

        servicio = Servicios.objects.get(id=id)
        return render(request, 'servicios/serviciosEditar.html', {'servicio': servicio})

    elif login and (login[4] != 'Administrador' or login[4] != 'Empleado'):
        messages.info(request, 'No tienes permisos para ingresar a este módulo')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debes iniciar sesión')
        return redirect('checho:login')


def guardadoServicio(request):
    """Esta funcion recibe unos parametros
     por metodo post y actualiza un servicio.

     Args:

        nomSer (str): Nombre del servicio
        precio (int): Precio del servicio
        descrip (str): Descripcion del servicio
        categoria (str):Categoria del servicio
        servicios (int): id del servicio

     Returns:

           html: Pagina de listado de  servicios.

     """
    try:
        if request.method == 'POST':

            nomSer = request.POST['nombre']
            precio = request.POST['precio']
            descrip = request.POST['descripcion']
            categoria = request.POST['categoria']

            servicios = Servicios.objects.get(id=request.POST['id'])

            servicios.nombreServicio = nomSer
            servicios.precio = precio
            servicios.descripcion = descrip
            servicios.categoria = categoria

            servicios.save()

            messages.success(request, 'Servicio editado')

            return redirect('checho:listarServicios')

        else:

            messages.warning(request, "Usted no envio datos ")
            return redirect('checho:listarServicios')

    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('checho:listarServicios')


# Portafolio
def portafolio(request, categoria):
    """Esta funcion renderiza el portafolio de servicios

    Args:
        categoria (str): Categoria del servicio.

    Returns:
        html: Pagina del portafolio del servicio.
    """
    portafolio = Servicios.objects.filter(categoria=categoria)
    contexto = {"portafolio": portafolio}
    return render(request, 'portafolio/portafolio.html', contexto)


#Modulo recuperar contraseña
def formularioRecuperarClave(request):
    """Esta funcion renderiza al formulario para validar el usuario y cambiar la contraseña.

    Args:
        No recibe ningun parametro.

    Returns:
        html: Formulario para cambiar contraseña.
    """
    return render(request, 'recuperarClave/recuperarClave.html')


def recuperarClave(request):

    """Esta funcion valida el usuario en la base de datos y renderiza al formulario para mandar el correo con la
    nueva contraseña.

    Args:
        user (str): Usuario
        palabraC (str): Palabra clave del usuario

    Returns:
        html: Formulario para enviar correo.

    """

    if request.method == 'POST':
        try:
            user = request.POST['user']
            palabraC = request.POST['palabraClave']

            q = Usuarios.objects.get(usuario=user, palabraClave=palabraC)

            if q is not None:
                return render(request, 'recuperarClave/mandarCorreo.html', {'usuario': q})
            else:
                messages.warning(request, 'Datos no coinciden')
                return redirect('checho:recuperarClave')


        except Exception:

            messages.warning(request, 'Datos no coinciden')
            return redirect('checho:login')


def mandarCorreo(request):

    """Esta funcion manda el correo con la nueva contraseña temporal

    Args:
        correo (str): Correo del usuario
        usuario (str): Id del usuario
        claveAleatoria (int): Clave nueva para el usuario

    Returns:
        mensaje: Correo enviado
        html: Renderiza al index

    """

    try:
        correo = request.POST["correo"]
        usuario = request.POST["usuario"]

        q = Usuarios.objects.get(pk=usuario)

        # clave aleatoria
        import random
        claveAleatoria = random.randint(100000, 999999)
        q.contraseña = claveEncriptada(str(claveAleatoria))
        q.save()

        #Enviar clave aleatoria al correo.
        send_mail(
            'Restablecer contraseña',
            f'Contraseña temporal: {claveAleatoria}, '
            f'cuando ingrese al sistema cambie la contraseña desde el apartado de perfil',
            'cristian.arboleda02@gmail.com',
            [f'{correo}'],
            fail_silently=False,
        )
        messages.info(request, 'Correo enviado')
        return redirect('checho:index')
    except Exception:
        return redirect('checho:mandarCorreo')


# Agendamiento

def agendaEmpleado(request):
    login = request.session.get('logueo', False)
    if login and login[4] == 'Administrador':
        q = Usuarios.objects.filter(rol='E')
        return render(request, 'agendamiento/agendaEmpleado.html', {'datos': q})

    elif login and login[4] != 'Administrador':
        messages.warning(request, 'No tiene permisos para acceder')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:index')


def guardadoAgenda(request):
    try:
        if request.method == 'POST':
            fechaInicio = request.POST['fechaInicio']
            fechaFin = request.POST['fechaFin']
            Empleado = request.POST['Empleado']

            emplea = Usuarios.objects.get(pk=Empleado)

            q = AgendaEmpleado.objects.create(empleado=emplea, fecha_inicio=fechaInicio, fecha_fin=fechaFin)

            messages.success(request, 'Agenda creada')

            return redirect('checho:agendamiento')

        else:

            messages.warning(request, "Usted no envio datos ")
            return redirect('checho:agendamiento')
    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('checho:agendamiento')


def agendamiento(request):
    login = request.session.get('logueo', False)
    if login and (login[4] == 'Administrador' or login[4] =='Empleado'):
        q = AgendaEmpleado.objects.raw(
            f"SELECT id, fecha_inicio,fecha_fin from checho_agendaempleado where empleado_id = {login[0]}  group by fecha_inicio;")
        todos = AgendaEmpleado.objects.all()
        contexto = {"datos": q, 'todos': todos}
        return render(request, 'agendamiento/listar.html', contexto)

    elif login and (login[4] != 'Administrador' or login[4] =='Empleado'):
        messages.warning(request, 'No tiene permisos para acceder')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:index')


def vistaAgendamientoS1(request, fecha, fechaf):
    login = request.session.get('logueo', False)
    if login and login[4] == 'Empleado':
        i = Usuarios.objects.get(pk=login[0])

        q = Disponibilidad.objects.filter(empleado=i, fecha_inicio=fecha, fecha_fin=fechaf,semana=1)
        contexto = {"datos": q, "fecha": fecha, "fechaf": fechaf}
        return render(request, 'agendamiento/vista_agendaS1.html', contexto)

    elif login and login[4] != 'Empleado':
        messages.warning(request, 'No tiene permisos para acceder')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:index')

def vistaAgendamientoS2(request, fecha, fechaf):
    login = request.session.get('logueo', False)
    if login and login[4] == 'Empleado':
        i = Usuarios.objects.get(pk=login[0])

        q = Disponibilidad.objects.filter(empleado=i, fecha_inicio=fecha, fecha_fin=fechaf, semana=2)
        contexto = {"datos": q, "fecha": fecha, "fechaf": fechaf}
        return render(request, 'agendamiento/vista_agendaS2.html', contexto)

    elif login and login[4] != 'Empleado':
        messages.warning(request, 'No tiene permisos para acceder')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:index')

def vistaAgendamientoS3(request, fecha, fechaf):
    login = request.session.get('logueo', False)
    if login and login[4] == 'Empleado':
        i = Usuarios.objects.get(pk=login[0])

        q = Disponibilidad.objects.filter(empleado=i, fecha_inicio=fecha, fecha_fin=fechaf, semana = 3)
        contexto = {"datos": q, "fecha": fecha, "fechaf": fechaf}
        return render(request, 'agendamiento/vista_agendaS3.html', contexto)

    elif login and login[4] != 'Empleado':
        messages.warning(request, 'No tiene permisos para acceder')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:index')

def vistaAgendamientoS4(request, fecha, fechaf):
    login = request.session.get('logueo', False)
    if login and login[4] == 'Empleado':
        i = Usuarios.objects.get(pk=login[0])

        q = Disponibilidad.objects.filter(empleado=i, fecha_inicio=fecha, fecha_fin=fechaf , semana = 4)
        contexto = {"datos": q, "fecha": fecha, "fechaf": fechaf}
        return render(request, 'agendamiento/vista_agendaS4.html', contexto)

    elif login and login[4] != 'Empleado':
        messages.warning(request, 'No tiene permisos para acceder')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:index')

def vistaSemana(request, fecha, fechaf):
    login = request.session.get('logueo', False)
    if login and login[4] == 'Empleado':
        i = Usuarios.objects.get(pk=login[0])

        q = Disponibilidad.objects.filter(empleado=i, fecha_inicio=fecha, fecha_fin=fechaf)
        contexto = {"datos": q, "fecha": fecha, "fechaf": fechaf}
        return render(request, 'agendamiento/semanas.html', contexto)

    elif login and login[4] != 'Empleado':
        messages.warning(request, 'No tiene permisos para acceder')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:index')


def actualizarAgendamiento(request, fecha, fechaf):
    login = request.session.get('logueo', False)
    i = Usuarios.objects.get(pk=login[0])
    if request.method == "POST":
        # Eliminamos toda la agenda del usuario y fecha

        """from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(f"DELETE from territorio_disponibilidad WHERE instructor_id = {login[0]} and fecha_inicio = {fecha}")
        """
        r = Disponibilidad.objects.filter(empleado_id=login[0], fecha_inicio=fecha, fecha_fin=fechaf)
        r.delete()

        for a in request.POST.getlist('agenda[]'):
            tmp = a.split('-')
            dia = tmp[0]
            hora = tmp[1]
            print(f"Dia: {dia} - Hora {hora}")
            # Hacemos sólo los inserts de los chequeados
            # pendiente..... día final del mes... <<<<<<<<<<<<
            q = Disponibilidad(empleado=i, dia=dia, hora=hora, fecha_inicio=fecha, fecha_fin=fechaf,semana=request.POST['semana'])
            q.save()
    else:
        messages.warning(request, "No se enviaron datos")
    messages.success(request, "Agenda actualizada correctamente!!")
    return redirect('checho:vistaSemana', fecha=fecha, fechaf=fechaf)

def verAgendamiento(request):
    login = request.session.get('logueo', False)
    if login and login[4] == 'Administrador':

        dis=Disponibilidad.objects.all()
        pag = Paginator(dis, 5)  # cinco registros por página
        page_number = request.GET.get('page')

        # sobreescribo el query
        dis = pag.get_page(page_number)

        contexto = {'page_obj': dis}

        return render(request,'usuario/disponibilidadTodos.html',{'page_obj':dis})

    elif login and login[4] != 'Administrador':
        messages.warning(request, 'No tiene permisos para acceder')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:index')


def apartarCita(request):
    login = request.session.get('logueo', False)
    if login and login[4] == 'Cliente':
        q = Usuarios.objects.filter(rol="E")
        contexto = {"datos": q}
        return render(request, 'agendamiento/apartar_cita.html', contexto)

    elif login and login[4] != 'Cliente':
        messages.warning(request, 'No tiene permisos para acceder')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:index')


def formularioApartarCita(request, empleado):
    login = request.session.get('logueo', False)
    if login and login[4] == 'Cliente':

        c = Usuarios.objects.get(pk=login[0])

        s=datetime.now()
        se=s.day
        print(f'este es el diaaaa {se}')

        if se <= 7:
            print(f'este es el 1 ')
            fecha = datetime.now()
            otra = datetime.now()
            # fecha = fecha.strftime('Día :%d, Mes: %m, Año: %Y, Hora: %H, Minutos: %M, Segundos: %S')
            otra = f"{fecha.year}-{fecha.month}-30"
            fecha = f"{fecha.year}-{fecha.month}-01"


            empeladoVitas=Usuarios.objects.get(pk=empleado)
            q = Disponibilidad.objects.filter(empleado=empleado, fecha_inicio=fecha, semana = 1, reservado=False,estado=0)

            contexto = {"datos": q, "fecha": fecha, 'usuario': c, 'empleado': empleado, 'fechaf': otra,'emple':empeladoVitas}
            return render(request, 'agendamiento/apartCita.html', contexto)

        elif se >= 8 and se < 15:
            fecha = datetime.now()
            otra = datetime.now()
            # fecha = fecha.strftime('Día :%d, Mes: %m, Año: %Y, Hora: %H, Minutos: %M, Segundos: %S')
            otra = f"{fecha.year}-{fecha.month}-30"
            fecha = f"{fecha.year}-{fecha.month}-01"

            empeladoVitas = Usuarios.objects.get(pk=empleado)
            q = Disponibilidad.objects.filter(empleado=empleado, fecha_inicio=fecha, semana=2, reservado=False, estado=0)
            contexto = {"datos": q, "fecha": fecha, 'usuario': c, 'empleado': empleado, 'fechaf': otra,
                        'emple': empeladoVitas}
            return render(request, 'agendamiento/apartCita.html', contexto)

        elif se >=15 and se < 22:
            print(f'este es el diaaaa 3')
            fecha = datetime.now()
            otra = datetime.now()
            # fecha = fecha.strftime('Día :%d, Mes: %m, Año: %Y, Hora: %H, Minutos: %M, Segundos: %S')
            otra = f"{fecha.year}-{fecha.month}-30"
            fecha = f"{fecha.year}-{fecha.month}-01"

            empeladoVitas = Usuarios.objects.get(pk=empleado)
            q = Disponibilidad.objects.filter(empleado=empleado, fecha_inicio=fecha, semana=3, reservado=False, estado=0)
            contexto = {"datos": q, "fecha": fecha, 'usuario': c, 'empleado': empleado, 'fechaf': otra,
                        'emple': empeladoVitas}
            return render(request, 'agendamiento/apartCita.html', contexto)
        else:
            print(f'este es el diaaaa 4')
            fecha = datetime.now()
            otra = datetime.now()
            # fecha = fecha.strftime('Día :%d, Mes: %m, Año: %Y, Hora: %H, Minutos: %M, Segundos: %S')
            otra = f"{fecha.year}-{fecha.month}-30"
            fecha = f"{fecha.year}-{fecha.month}-01"

            empeladoVitas = Usuarios.objects.get(pk=empleado)
            q = Disponibilidad.objects.filter(empleado=empleado, fecha_inicio=fecha, semana=4, reservado=False, estado=0)
            contexto = {"datos": q, "fecha": fecha, 'usuario': c, 'empleado': empleado, 'fechaf': otra,
                        'emple': empeladoVitas}
            return render(request, 'agendamiento/apartCita.html', contexto)

    elif login and login[4] != 'Cliente':
        messages.warning(request, 'No tiene permisos para acceder')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:index')

def guardarDia(request):
    global result
    login = request.session.get('logueo', False)
    if login and login[4] == 'Cliente':

        c = Usuarios.objects.get(pk=login[0])
        #dia = request.POST['dia']
        emplea = request.POST['empleado']
        d = request.POST['dias']

        diasSemana={ 0:'L',1:'M',2:'X',3:'J',4:'V',5:'S',6:'D'}

        for i in diasSemana:
            if d == diasSemana[i]:
                result=i
                break

        hoy = datetime.now().weekday()
        if result < hoy or result == hoy:
            messages.error(request, 'El dia no esta disponible...')
            print(result)
            print(hoy)
            return redirect('checho:formularioApartarCita', emplea)

        try:
            dia=Disponibilidad.objects.filter(dia=request.POST['dias'],empleado=emplea)
            if dia:
                dia=request.POST['dias']
            else:
                messages.error(request, 'El dia no esta disponible ')
                return  redirect('checho:formularioApartarCita', emplea)
        except :
            messages.error(request, 'El dia no esta disponible para el empleado')
            return redirect('checho:formularioApartarCita', emplea)

        q = Disponibilidad.objects.filter(empleado=emplea, dia=dia, estado=0, reservado=False)
        contexto = {'datos': q , 'dia': dia,'empleado': emplea, 'fecha': request.POST['fecha'], 'fechaf': request.POST['fechaf']}
        return render(request, 'agendamiento/apartHora.html', contexto)

    elif login and login[4] != 'Cliente':
        messages.warning(request, 'No tiene permisos para acceder')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:index')

def guardarCitacion(request):

    login = request.session.get('logueo', False)
    dia = request.POST['dia']
    hora = request.POST['hora']
    fecha = request.POST['fecha']
    fechaf = request.POST['fechaf']

    empleado=Usuarios.objects.get(pk=request.POST['empleado'])
    cliente = Usuarios.objects.get(pk=login[0])
    q = Disponibilidad.objects.filter(empleado=empleado, dia=dia, hora=hora, fecha_inicio=fecha, fecha_fin=fechaf)
    q.delete()

    try:
        q = Disponibilidad(empleado=empleado, dia=dia, hora=hora, fecha_inicio=fecha, fecha_fin=fechaf, reservado=True, estado=1)
        q.save()
        c = Citas(dia=dia, hora=hora, usuarioCliente=cliente, usuarioEmpleado=empleado)
        c.save()

        messages.success(request, 'Cita Agandada con exito')
        return redirect('checho:verMiCita')

    except Exception as e:

        messages.error(request, 'No se puedo agendar la cita')
        return redirect('checho:agendamiento')


def listarClientes(request):
    login = request.session.get('logueo', False)
    if login and login[4] == 'Empleado':
        q = Usuarios.objects.filter(rol="C")
        pag = Paginator(q, 5)  # cinco registros por página
        page_number = request.GET.get('page')

        # sobreescribo el query
        q = pag.get_page(page_number)

        contexto = {'page_obj': q}
        return render(request, 'usuario/listarClientes.html', contexto)

    elif login and login[4] != 'Empleado':
        messages.warning(request, 'No tiene permisos para acceder')
        return redirect('checho:index')

    else:
        messages.warning(request, 'Debe iniciar sesión')
        return redirect('checho:index')

def eliminarCita(request,id):
    global result2

    q=Citas.objects.get(id=id)
    d=Disponibilidad.objects.get(empleado=q.usuarioEmpleado,dia=q.dia,hora=q.hora)

    diasSemana = {0: 'L', 1: 'M', 2: 'X', 3: 'J', 4: 'V', 5: 'S', 6: 'D'}

    for i in diasSemana:
        if q.dia == diasSemana[i]:
            result2 = i
            break

    hoy = datetime.now().weekday()
    print(hoy)
    print(result2)
    if hoy <result2:
        try:
            if d is not None:
                d.reservado=False
                d.estado=0
                d.save()
                q.delete()

                messages.info(request, 'cita eliminada ')
                return redirect('checho:verMiCita')

        except Exception as e:

            messages.warning(request,  e )
            return redirect('checho:verMiCita')
    else:

        messages.error(request, 'debes cancelar la cita minimo con un dia de antelacion ')
        return redirect('checho:verMiCita')