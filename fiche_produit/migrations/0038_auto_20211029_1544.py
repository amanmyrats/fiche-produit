# Generated by Django 3.2.6 on 2021-10-29 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_produit', '0037_auto_20211028_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcard',
            name='rooms',
            field=models.ManyToManyField(blank=True, null=True, through='fiche_produit.ProductCardRoom', to='fiche_produit.Room'),
        ),
        migrations.AlterField(
            model_name='productcardannexe5',
            name='annexe5',
            field=models.ManyToManyField(blank=True, to='fiche_produit.Annexe5'),
        ),
        migrations.AlterField(
            model_name='productcardannexe5',
            name='productcard',
            field=models.ManyToManyField(blank=True, to='fiche_produit.ProductCard'),
        ),
        migrations.RemoveField(
            model_name='productcardroom',
            name='productcard',
        ),
        migrations.AddField(
            model_name='productcardroom',
            name='productcard',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='fiche_produit.productcard'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='productcardroom',
            name='room',
        ),
        migrations.AddField(
            model_name='productcardroom',
            name='room',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='fiche_produit.room'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='productcardroom',
            constraint=models.UniqueConstraint(fields=('productcard', 'room'), name='productcard-room'),
        ),
    ]
