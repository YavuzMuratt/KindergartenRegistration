# Generated by Django 5.1 on 2024-08-26 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kindergarten_registration', '0017_alter_ogrenci_tercih_edilen_okul'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ogrenci',
            name='tercih_edilen_okul',
            field=models.CharField(blank=True, default='None', max_length=100, null=True),
        ),
    ]
