# Generated by Django 3.2.6 on 2021-10-01 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_produit', '0002_rename_specificaionitem_specificationitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='client',
        ),
        migrations.AddField(
            model_name='client',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fiche_produit.project'),
        ),
    ]
