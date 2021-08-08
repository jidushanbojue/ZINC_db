# from django.db import models

# Create your models here.
from django_rdkit import models
from django.contrib.postgres.indexes import GistIndex


class Compound(models.Model):
    zinc_name = models.CharField(max_length=200, blank=True, null=True)
    molecule = models.MolField(null=True)

    atom_count = models.IntegerField(null=True)
    bond_count = models.IntegerField(null=True)
    torsionbv = models.BfpField(null=True)
    mfp2 = models.BfpField(null=True)
    ffp2 = models.BfpField(null=True)

    def __str__(self):
        return self.zinc_name

    class Meta:
        indexes = [
            GistIndex(fields=['molecule']),
            GistIndex(fields=['mfp2'])
        ]



