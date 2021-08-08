import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZINC_db.settings')
import django
django.setup()

from django_rdkit.models import *
from database.models import *

def smiles_substructure_query(substructure):
     query = Compound.objects.filter(molecule__hassubstruct=substructure)
     for cmpd in query.annotate(smiles=MOL_TO_SMILES('molecule'))[:5]:
         print(cmpd.zinc_name, cmpd.smiles)


# smiles_substructure_query('c1cccc2c1nncc2')

smiles = 'Cc1ccc2nc(-c3ccc(NC(C4N(C(c5cccs5)=O)CCC4)=O)cc3)sc2c1'
value = MORGANBV_FP(Value(smiles))
Compound.objects.filter(mfp2__tanimoto=value).count()


