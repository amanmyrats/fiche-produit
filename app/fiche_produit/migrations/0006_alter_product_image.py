# Generated by Django 3.2.6 on 2021-10-02 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_produit', '0005_auto_20211001_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_image/'),
        ),
    ]
