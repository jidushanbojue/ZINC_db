# ZINC database substructure search and similarity search

## Create enviroment
* conda create -f requirement.yml
* pip install git+https://github.com/rdkit/django-rdkit.git

* input_file contain two colunms "smiles" and 'names'
## substructure search for smiles (no stereochemistry)
* python substructure_search.py -I input_file -O output_file -t smiles

## substructure search for smiles (contain stereochemistry)
* python substructure_search.py -I input_file -O output_file -t smiles -stereo

## substructure search for smarts (whether stereochemistry or not)
* python substructure_search.py -I input_file -O output_file -t smarts

## similarity search for smiles (default tanimoto value: 0.5)
* python substructure_search.py -I input_file -O output_file -t similarity -tt 0.5