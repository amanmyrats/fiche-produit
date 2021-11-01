# Generated by Django 3.2.6 on 2021-11-01 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_produit', '0040_auto_20211101_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcard',
            name='location_ru',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='productcard',
            name='observation_ru',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='productcard',
            name='protocol_ru',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
