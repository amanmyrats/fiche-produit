# Generated by Django 3.2.6 on 2021-10-02 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_produit', '0011_auto_20211002_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facture',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='facture',
            name='price',
        ),
        migrations.RemoveField(
            model_name='facture',
            name='total_price',
        ),
    ]