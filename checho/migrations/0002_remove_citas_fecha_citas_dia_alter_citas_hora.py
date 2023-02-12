# Generated by Django 4.1.3 on 2022-12-06 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checho', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citas',
            name='fecha',
        ),
        migrations.AddField(
            model_name='citas',
            name='dia',
            field=models.CharField(choices=[('L', 'Lunes'), ('M', 'Martes'), ('X', 'Miércoles'), ('J', 'Jueves'), ('V', 'Viernes'), ('S', 'Sábado'), ('D', 'Domingo')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='citas',
            name='hora',
            field=models.IntegerField(choices=[(11, '11AM'), (12, '12M'), (13, '1PM'), (14, '2PM'), (15, '3PM'), (16, '4PM'), (17, '5PM')], default=''),
        ),
    ]