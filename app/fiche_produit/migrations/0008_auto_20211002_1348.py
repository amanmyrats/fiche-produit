# Generated by Django 3.2.6 on 2021-10-02 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fiche_produit', '0007_room_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=3, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='productcard',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fiche_produit.department'),
        ),
        migrations.AlterField(
            model_name='productcard',
            name='phase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fiche_produit.phase'),
        ),
        migrations.AlterField(
            model_name='productcard',
            name='trade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fiche_produit.trade'),
        ),
    ]