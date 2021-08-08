import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZINC_db.settings')
import django
django.setup()

from rdkit import Chem
import pandas as pd
from multiprocessing import Pool
from database.models import ZINC_DB

def work(zinc_info):
    smiles, name, atom_count, bond_count = zinc_info[0], zinc_info[1], zinc_info[2], zinc_info[3]
    molecule = Chem.MolFromSmiles(smiles)
    if molecule:
        # smi = Chem.MolToSmiles(molecule)
        # test_molecule = Chem.MolFromSmiles(smi)
        # if not test_molecule:
        #     print('')
        return ZINC_DB(zinc_name=name, molecule=molecule, atom_count=atom_count, bond_count=bond_count)
    else:
        return ''

from itertools import islice


def upload(zinc_file, batch_size=100000):
    df = pd.read_csv(zinc_file)
    # for idx, line in df.iterrows():
    #     smiles, name, atom_count, bond_count = line['Molecule'], line
    info_list = list(zip(df['Molecule'], df['Molecule name'], df['Atom count'], df['Bond count']))

    p = Pool(160)
    res = p.map(work, info_list)
    p.close()
    p.join()
    print('generate obj done')

    # objs = ZINC_DB.objects.bulk_create(res)
    objs = [obj for obj in res if obj != '']
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        ZINC_DB.objects.bulk_create(batch, batch_size)



# if __name__ == '_main__':
#     file_dir = '../data/zinc_all_data_top10000.csv'
#     upload(file_dir)

# file_dir = '../data/zinc_all_data_top10000.csv'
file_dir = 'data/zinc_all_data.csv'
upload(file_dir)



