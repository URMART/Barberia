from django.urls import path
from . import views

app_name='checho'

urlpatterns = [

    path("", views.index,name='index'),

    #login
    path('loginFormulario/', views.loginFormulario,name='loginFormulario'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout,name='logout'),

    #usuarios
    path('listarUsuarios/', views.listarUsuarios,name='listarUsuarios'),
    path('eliminarUser/<int:id>', views.eliminarUser,name='eliminarUser'),
    path('registrarUsuario/', views.registrarUsuario,name='registrarUsuario'),
    path('guardarUsuario/', views.guardarUsuario,name='guardarUsuario'),
    path('editarUsuarios/<int:id>', views.editarUsuarios,name='editarUsuarios'),
    path('guardadoUsuario/', views.guardadoUsuario,name='guardadoUsuario'),
    path('perfil/', views.perfil,name='perfil'),
    path('actualizarPerfil/', views.actualizarPerfil,name='actualizarPerfil'),
    path('verMiCita/', views.verMiCita, name='verMiCita'),
    path('verAgendaEmpleado/', views.verAgendaEmpleado, name='verAgendaEmpleado'),
    path('listarClientes/', views.listarClientes, name='listarClientes'),
    path('eliminarCita/<int:id>', views.eliminarCita, name='eliminarCita'),

    #Servicios
    path('listarServicios/', views.servicios, name='listarServicios'),
    path('registrarServicio/', views.registrarServicio,name='registrarServicio'),
    path('guardarServicio/', views.guardarServicio,name='guardarServicio'),
    path('eliminarServicio/<int:id>', views.eliminarServicio,name='eliminarServicio'),
    path('editarServicio/<int:id>', views.editarServicio,name='editarServicio'),
    path('guardadoServicio/', views.guardadoServicio,name='guardadoServicio'),

    


    #Datos portafolio
    path('portafolio/<str:categoria>', views.portafolio, name='portafolio'),

    #AGENDAN
    path('agendaEmpleado/', views.agendaEmpleado, name="agendaEmpleado"),
    path('guardadoAgenda/', views.guardadoAgenda, name="guardadoAgenda"),
    path('agendamiento/', views.agendamiento, name="agendamiento"),
    path('vistaSemana/<str:fecha>/<str:fechaf>', views.vistaSemana, name="vistaSemana"),
    path('vistaAgendamientoS1/<str:fecha>/<str:fechaf>', views.vistaAgendamientoS1, name="vistaAgendamientoS1"),
    path('vistaAgendamientoS2/<str:fecha>/<str:fechaf>', views.vistaAgendamientoS2, name="vistaAgendamientoS2"),
    path('vistaAgendamientoS3/<str:fecha>/<str:fechaf>', views.vistaAgendamientoS3, name="vistaAgendamientoS3"),
    path('vistaAgendamientoS4/<str:fecha>/<str:fechaf>', views.vistaAgendamientoS4, name="vistaAgendamientoS4"),

    path('actualizarAgendamiento/<str:fecha>/<str:fechaf>/', views.actualizarAgendamiento, name="actualizarAgendamiento"),
    path('apartarCita/', views.apartarCita, name="apartarCita"),
    path('formularioApartarCita/<int:empleado>', views.formularioApartarCita, name="formularioApartarCita"),
    path('guardarDia/', views.guardarDia, name="guardarDia"),
    path('guardarCitacion/', views.guardarCitacion, name="guardarCitacion"),
    path('verAgendamiento/', views.verAgendamiento, name="verAgendamiento"),

    # recuperar contraseña
    path('formRecuperarClave/', views.formularioRecuperarClave, name='formRecuperarClave'),
    path('recuperarClave/', views.recuperarClave, name='recuperarClave'),
    path('mandarCorreo/', views.mandarCorreo, name='mandarCorreo'),





]
