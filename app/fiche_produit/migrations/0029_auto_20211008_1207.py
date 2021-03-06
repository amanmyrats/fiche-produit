# Generated by Django 3.2.6 on 2021-10-08 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_produit', '0028_productcard_fp_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='annexe5',
        ),
        migrations.AddField(
            model_name='productcard',
            name='annexe5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fiche_produit.annexe5'),
        ),
        migrations.AlterField(
            model_name='productcard',
            name='observation',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='productcard',
            name='protocol',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
