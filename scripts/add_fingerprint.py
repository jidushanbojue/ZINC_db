import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZINC_db.settings')
import django
django.setup()

from database.models import Compound
from django_rdkit.models import *

Compound.objects.update(
    torsionbv=TORSIONBV_FP('molecule'),
    mfp2=MORGANBV_FP('molecule'),
    ffp2=FEATMORGANBV_FP('molecule'),
)
print('Done')
