# Generated by Django 3.2.6 on 2021-08-07 13:27

from django.db import migrations
import django_rdkit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_create_compound_molecule_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='zinc_db',
            name='ffp2',
            field=django_rdkit.models.fields.BfpField(null=True),
        ),
        migrations.AddField(
            model_name='zinc_db',
            name='mfp2',
            field=django_rdkit.models.fields.BfpField(null=True),
        ),
        migrations.AddField(
            model_name='zinc_db',
            name='torsionbv',
            field=django_rdkit.models.fields.BfpField(null=True),
        ),
    ]