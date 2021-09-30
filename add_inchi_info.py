import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZINC_db.settings')
import django
django.setup()

from rdkit import Chem
import pandas as pd
from multiprocessing import Pool
from database.models import Compound

def work(id):
    query = Compound.objects.get(id=id)
    query.inchi = Chem.MolToInchi(query.molecule)
    query.inchikey = Chem.MolToInchiKey(query.molecule)
    query.save()

def main():
    # for cpd in Compound.objects.get(id):
    #     print(cpd.zinc_name)
    id_list = range(1, 12389285)
    # for id in id_list:
    #     work(id)


    p = Pool(160)
    result = p.map(work, id_list)
    p.close()
    p.join()

main()

# q = Compound.objects.get(id=1)
# q.inchi = Chem.MolToInchi(q.molecule)
# q.save()
# print(Chem.MolToInchi(q.molecule))
# print(Chem.MolToInchiKey(q.molecule))
# print('done')






