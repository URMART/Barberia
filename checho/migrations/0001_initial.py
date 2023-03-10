# Generated by Django 4.1.3 on 2022-12-05 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Citas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Servicios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreServicio', models.CharField(max_length=255)),
                ('descripcion', models.CharField(max_length=255)),
                ('precio', models.PositiveIntegerField()),
                ('categoria', models.CharField(max_length=100)),
                ('foto', models.ImageField(default='checho/fotos/default2.png', upload_to='checho/fotos')),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('numeroTelefono', models.PositiveIntegerField()),
                ('usuario', models.CharField(max_length=100)),
                ('contraseña', models.CharField(max_length=100)),
                ('correo', models.CharField(default='', max_length=100)),
                ('palabraClave', models.CharField(default='', max_length=40)),
                ('rol', models.CharField(choices=[('C', 'Cliente'), ('E', 'Empleado'), ('A', 'Administrador')], default='C', max_length=1)),
                ('foto', models.ImageField(default='checho/fotos/default.png', upload_to='checho/fotos')),
            ],
        ),
        migrations.CreateModel(
            name='ServiciosCitas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='checho.citas')),
                ('servicios', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='checho.servicios')),
            ],
        ),
        migrations.CreateModel(
            name='Disponibilidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(choices=[('L', 'Lunes'), ('M', 'Martes'), ('X', 'Miércoles'), ('J', 'Jueves'), ('V', 'Viernes'), ('S', 'Sábado'), ('D', 'Domingo')], max_length=1)),
                ('hora', models.IntegerField(choices=[(11, '11AM'), (12, '12M'), (13, '1PM'), (14, '2PM'), (15, '3PM'), (16, '4PM'), (17, '5PM')])),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('reservado', models.BooleanField(default=False)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='checho.usuarios')),
            ],
        ),
        migrations.AddField(
            model_name='citas',
            name='usuarioCliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuarioCliente', to='checho.usuarios'),
        ),
        migrations.AddField(
            model_name='citas',
            name='usuarioEmpleado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuarioEmpleado', to='checho.usuarios'),
        ),
        migrations.CreateModel(
            name='AgendaEmpleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='checho.usuarios')),
            ],
        ),
    ]
