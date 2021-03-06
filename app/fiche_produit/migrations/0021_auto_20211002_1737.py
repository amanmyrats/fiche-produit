# Generated by Django 3.2.6 on 2021-10-02 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_produit', '0020_auto_20211002_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factureitem',
            name='no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddConstraint(
            model_name='factureitem',
            constraint=models.UniqueConstraint(fields=('facture', 'no'), name='facture-item-no'),
        ),
    ]
