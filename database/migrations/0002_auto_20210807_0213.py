# Generated by Django 3.2.6 on 2021-08-07 02:13

from django.db import migrations, models
import django_rdkit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='zinc_db',
            name='atom_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='zinc_db',
            name='bond_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='zinc_db',
            name='molecule',
            field=django_rdkit.models.fields.MolField(null=True),
        ),
    ]
