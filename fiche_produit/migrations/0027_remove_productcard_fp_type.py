# Generated by Django 3.2.6 on 2021-10-08 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_produit', '0026_auto_20211008_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcard',
            name='fp_type',
        ),
    ]
