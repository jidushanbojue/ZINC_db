import os
import argparse
import os

import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZINC_db.settings')
import django
django.setup()

from database.models import *
from django_rdkit.models import *
from django_rdkit.config import config
import argparse
from rdkit import Chem


def parse_arguments():
    parser = argparse.ArgumentParser(description='Search molecules from ZINC database')
    parser.add_argument('-I', '--input-mol', dest='infile', required=True, help='Specify the absolute path to the input file')
    parser.add_argument('-O', '--output-file', dest='outfile', required=True, help='Specify the filename for the output file')

    parser.add_argument('-t', '--type', default=None, help='Specify the smiles or smarts searching process')
    parser.add_argument('-stereo', type=bool, default=False, help='Only for Smiles search (when -t smiles) Specify whether do stereochemistry search for ')

    parser.add_argument('-tt', '--tanimoto-threshold', type=float, default=0.5, help='Only for Smiles similarity search')

    # smi_search_group = parser.add_argument_group('smiles-search')
    # smi_search_group.add_argument('--type', default='smiles')
    # smi_search_group.add_argument('--stereo', default=False)
    #
    # smr_search_group = parser.add_argument_group('smarts-search')
    # smr_search_group.add_argument('--type', default='smarts')


    # args = parser.parse_args([
    #     '-I', '/data/baiqing/PycharmProjects/ZINC_db/data/zinc_test.csv',
    #     '-O', '/data/baiqing/PycharmProjects/ZINC_db/data/zinc_test_result.csv',
    #     '-t', 'similarity',
    #     '-tt', '0.4'
    # ])
    args = parser.parse_args()
    return args


def smiles_substructure_query(substructure, stereochemistry=None):
    if stereochemistry:
        config.do_chiral_sss = True
    else:
        config.do_chiral_sss = False

    result = []
    query = Compound.objects.filter(molecule__hassubstruct=substructure)
    for cmpd in query.annotate(smiles=MOL_TO_SMILES('molecule')):
        print(cmpd.zinc_name, cmpd.smiles)
        result.append((substructure, cmpd.zinc_name, cmpd.smiles))
    return result

def smarts_substructure_query(substructure, stereochemistry=False):
    query = Compound.objects.filter(molecule__hassubstruct=QMOL(Value(substructure)))
    result = []
    for cmpd in query.annotate(smiles=MOL_TO_SMILES('molecule')):
        print(cmpd.zinc_name, cmpd.smiles)
        result.append((substructure, cmpd.zinc_name, cmpd.smiles))
    return result

def get_mfp2_neighbors(smiles):
    value = MORGANBV_FP(Value(smiles))
    queryset = Compound.objects.filter(mfp2__tanimoto=value)
    queryset = queryset.annotate(smiles=MOL_TO_SMILES('molecule'))
    queryset = queryset.annotate(sml=TANIMOTO_SML('mfp2', value))
    queryset = queryset.order_by(TANIMOTO_DIST('mfp2', value))
    queryset = queryset.values_list('zinc_name', 'smiles', 'sml')
    return queryset

def similarity_query(smiles, tanimoto=0.5):
    config.tanimoto_threshold = tanimoto
    query = get_mfp2_neighbors(smiles)

    result = []
    for name, query_smi, sml in query:
        result.append((smiles, name, query_smi, sml))
    return result

# def save(result, outfile):
#     df = pd.DataFrame(result)
#     df.to_csv(outfile)



def create_mol_supplier(infile):
    """
    Take the input filename and based on extension, return the relevant RDKit
    supplier object.

    Args:
        infile (string):  name of input file

    Returns:
        RDKit mol supplier
    """

    # if infile.endswith('.smi') or infile.endswith('.smi.gz'):
    #     return Chem.SmilesMolSupplier(infile)
    # elif infile.endswith('.sdf') or infile.endswith('.sdf.gz'):
    #     return Chem.SDMolSupplier(infile)
    # elif infile.endswith('.sdf'):
    #     return Chem.SDMolSupplier(infile)
    info_list = []
    df = pd.read_csv(infile, names=['smiles', 'name'], header=None)
    for idx, line in df.iterrows():
        # mol = Chem.MolFromSmiles(line['smiles'].split("'")[1])
        mol = Chem.MolFromSmiles(line['smiles'])
        if mol:
            # yield Chem.MolToSmiles(mol), line['name']
            info_list.append(((Chem.MolToSmiles(mol), line['name'])))
        else:
            print('Error - unrecognized {} structure'.format(line['name']))
    return info_list
    # return None

def main():
    args = parse_arguments()
    # args = parser.parse_args(['-f', '/data/baiqing/PycharmProjects/ZINC_db/data/zinc_test.smi'])
    print('Read from {}'.format(args.infile))
    print('Write to {}'.format(args.outfile))
    search_type = args.type
    outfile = args.outfile
    stero = args.stereo
    tanimoto = args.tanimoto_threshold

    suppl = create_mol_supplier(args.infile)
    # if not suppl:
    #     print('Error - unrecognized file format for {}'.format(args.inifile))
    #     exit(1)
    # with open(args.outfile, 'w') as of:
    df = pd.DataFrame()
    for smiles, name in suppl:

        if search_type == 'smiles':
            result = smiles_substructure_query(smiles, stero)
        if search_type == 'smarts':
            result = smarts_substructure_query(smiles)

        if search_type == 'similarity':
            result = similarity_query(smiles, tanimoto)

        temp_df = pd.DataFrame(result)
        df = pd.concat([df, temp_df])
    df.to_csv(outfile)
main()








# smiles_substructure_query('c1cccc2c1nncc2')
# print('Done')
# smiles = 'Cc1ccc2nc(-c3ccc(NC(C4N(C(c5cccs5)=O)CCC4)=O)cc3)sc2c1'
# value = MORGANBV_FP(Value(smiles))
# num = Compound.objects.filter(mfp2__tanimoto=value).count()
# print(num)

#
# qs = get_mfp2_neighbors('c1ccccc1')
# print(qs.query)

# for name, smiles, sml in get_mfp2_neighbors('Cc1ccc2nc(-c3ccc(NC(C4N(C(c5cccs5)=O)CCC4)=O)cc3)sc2c1')[:10]:
#     print(name, smiles, sml)

# print(get_mfp2_neighbors('Cc1ccc2nc(N(C)CC(=O)O)sc2c1').count())
# print('Done')
# config.tanimoto_threshold = 0.7
#
# print(get_mfp2_neighbors('Cc1ccc2nc(N(C)CC(=O)O)sc2c1').count())
#
# config.tanimoto_threshold = 0.6
#
# print(get_mfp2_neighbors('Cc1ccc2nc(N(C)CC(=O)O)sc2c1').count())
#
# config.tanimoto_threshold = 0.5
#
# print(get_mfp2_neighbors('Cc1ccc2nc(N(C)CC(=O)O)sc2c1').count())
#
#











