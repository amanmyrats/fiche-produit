# Generated by Django 3.2.6 on 2021-11-01 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_produit', '0039_auto_20211029_1548'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productcard',
            old_name='location',
            new_name='location_fr',
        ),
        migrations.RenameField(
            model_name='productcard',
            old_name='observation',
            new_name='observation_fr',
        ),
        migrations.RenameField(
            model_name='productcard',
            old_name='protocol',
            new_name='protocol_fr',
        ),
        migrations.AddField(
            model_name='productcard',
            name='level',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='productcard',
            name='zone',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]