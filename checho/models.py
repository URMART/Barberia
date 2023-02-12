from django.db import models


class Usuarios(models.Model):
    """Esta clase sirve de esquema para
    el modelo usuarios en la base de datos.

    Args:
        nombre (str): Nombre de usuario
        apellido (str): Apellido del usuario
        numeroTelefono (int): Numero  de telefono
        usuario   (str): usuario
        contraseña (str): Contraseña
        rol (str): Rol de usuario
        foto (file): Foto del usuario

    Returns:

          Models: Modelos de Usuarios.
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numeroTelefono = models.PositiveIntegerField()
    usuario = models.CharField(max_length=100,unique=True)
    contraseña = models.CharField(max_length=100)
    correo = models.CharField(max_length=100, default='')
    palabraClave = models.CharField(max_length=40, default='')
    ROLES = (
        ("C", "Cliente"),
        ("E", "Empleado"),
        ("A", "Administrador"),
    )
    rol = models.CharField(choices= ROLES, max_length=1, default="C")
    foto = models.ImageField(upload_to = 'checho/fotos', default = 'checho/fotos/default.png') 

    def __str__(self) -> str:

        return f" {self.nombre} {self.apellido}  "



class Citas(models.Model):
    """Esta clase sirve de esquema para
    el modelo  citas en la base de datos.

    Args:
        fecha (date): Fecha de la cita
        hora (time): Hora de la cita
        estado (boolean): Estado de la cita
        usuarioCliente (str): Cliente de la cita
        usuarioEmpleado (str): Empleado para la cita

    Returns:
        Model: Modelos de la citas.
    """

    DIAS = (
        ('L', 'Lunes'),
        ('M', 'Martes'),
        ('X', 'Miércoles'),
        ('J', 'Jueves'),
        ('V', 'Viernes'),
        ('S', 'Sábado'),
        ('D', 'Domingo'),
    )
    dia = models.CharField(max_length=1, choices=DIAS,default='')
    HORAS = (
        (11, '11AM'),
        (12, '12M'),
        (13, '1PM'),
        (14, '2PM'),
        (15, '3PM'),
        (16, '4PM'),
        (17, '5PM'),
    )
    hora = models.IntegerField(choices=HORAS,default='')
    estado=models.BooleanField(default=True)
    usuarioCliente=models.ForeignKey(Usuarios, on_delete=models.CASCADE,null=True,related_name="usuarioCliente")
    usuarioEmpleado=models.ForeignKey(Usuarios, on_delete=models.CASCADE,null=True,related_name="usuarioEmpleado")


    def __str__(self):

        return  f"   {self.dia} {self.hora} {self.usuarioCliente}"




class Servicios(models.Model):
    """Esta clase sirve de esquema para
    el modelo  servicios en la base de datos.

    Args:
        nombreServicio (str): Nombre del servicio
        descripcion (str): Descripcion del servicio
        precio (int): Precio del servicio
        categoria (str)categoria: Categoria del servicio
        foto (int): Foto del servicio

    Returns:
          Model: Modelo de Servicios.

    """
    nombreServicio=models.CharField(max_length=255)
    descripcion=models.CharField(max_length=255)
    precio=models.PositiveIntegerField()
    categoria=models.CharField(max_length=100)
    foto = models.ImageField(upload_to = 'checho/fotos', default = 'checho/fotos/default.png')


    def __str__(self) -> str:
        return self.nombreServicio


class Disponibilidad(models.Model):
    """ Para el agendamiento del empleado """
    empleado = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING)
    DIAS = (
        ('L', 'Lunes'),
        ('M', 'Martes'),
        ('X', 'Miércoles'),
        ('J', 'Jueves'),
        ('V', 'Viernes'),
        ('S', 'Sábado'),
        ('D', 'Domingo'),
    )
    dia = models.CharField(max_length=1, choices=DIAS)
    HORAS = (
        (11, '11AM'),
        (12, '12M'),
        (13, '1PM'),
        (14, '2PM'),
        (15, '3PM'),
        (16, '4PM'),
        (17, '5PM'),
    )
    hora = models.IntegerField(choices=HORAS)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    reservado = models.BooleanField(default=False)
    estado = models.IntegerField(default='0')
    semana = models.IntegerField(default='0')

    def __str__(self):
        return f"{self.id} - {self.empleado}"

class AgendaEmpleado(models.Model):
    """ Para el agendamiento del empleado """
    empleado = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"{self.id} - {self.empleado}"