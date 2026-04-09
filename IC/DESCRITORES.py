import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem, PandasTools
import numpy as np

df = pd.read_csv('/home/mugazevedo05/MOLECULAS/CID_n_otm/SMILES/RDKIT/DADOS/SMILES_TUNING.csv', sep = ',')

PandasTools.AddMoleculeColumnToFrame(df, smilesCol='SMILES', molCol = 'ROMol')

def descritores(mol):

	AllChem.ComputeGasteigerCharges(mol)

	try:
		cargas = []

		for atom in mol.GetAtoms():
			charge = atom.GetDoubleProp("_GasteigerCharge")
			cargas.append(charge)

		max_charge = max(cargas)
		min_charge = min(cargas)

	except KeyError:
		max_charge = np.nan
		min_charge = np.nan


	res = {
		'MW' : Descriptors.MolWt(mol),
		'LogP' : Descriptors.MolLogP(mol),
		'MR' : Descriptors.MolMR(mol),
		'TPSA' : Descriptors.TPSA(mol),
		'NumAromaticRings' : Descriptors.NumAromaticRings(mol),
		'FractionCSP3' : Descriptors.FractionCSP3(mol),
		'NumValenceElectron' : Descriptors.NumValenceElectrons(mol),
		'MaxCharge' : max_charge,
		'MinCharge' : min_charge,
		'BertzCT' : Descriptors.BertzCT(mol),
		'BalabanJ' : Descriptors.BalabanJ(mol),
		'LabuteASA' : Descriptors.LabuteASA(mol)
		}

	return res

print('Extraindo descritores das quinonas')

descritores_lista = df['ROMol'].apply(descritores).tolist()

df_descritores = pd.DataFrame(descritores_lista)
df_final = pd.concat([df[['SMILES', 'CID']], df_descritores], axis = 1)

df_final.to_csv('QUINONAS_DESCRITORES.csv')

print(f'Gerado dataframe com descritores: QUINONAS_DESCRITORES.csv')
