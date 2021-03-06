# Generated by Django 3.2.6 on 2021-10-28 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_produit', '0035_alter_fptype_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCardRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('productcard', models.ManyToManyField(blank=True, null=True, to='fiche_produit.ProductCard')),
                ('room', models.ManyToManyField(blank=True, null=True, to='fiche_produit.Room')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCardAnnexe5',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('annexe5', models.ManyToManyField(blank=True, null=True, to='fiche_produit.Annexe5')),
                ('productcard', models.ManyToManyField(blank=True, null=True, to='fiche_produit.ProductCard')),
            ],
        ),
    ]
