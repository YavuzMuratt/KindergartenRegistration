# Generated by Django 5.1 on 2024-08-28 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kindergarten_registration', '0020_alter_ogrenci_tercih_edilen_okul'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sınıf',
            name='students',
            field=models.ManyToManyField(related_name='sinif_students', to='kindergarten_registration.ogrenci'),
        ),
    ]
