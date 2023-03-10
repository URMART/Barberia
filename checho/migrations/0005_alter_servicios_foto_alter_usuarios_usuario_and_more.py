# Generated by Django 4.1.2 on 2022-12-09 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checho', '0004_disponibilidad_semana'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicios',
            name='foto',
            field=models.ImageField(default='checho/fotos/default.png', upload_to='checho/fotos'),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='usuario',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.DeleteModel(
            name='ServiciosCitas',
        ),
    ]
