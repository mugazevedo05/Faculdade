from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import PandasTools
import pandas as pd

df = pd.read_csv('/home/mugazevedo05/MOLECULAS/CID_n_otm/SMILES/RDKIT/DADOS/SMILES_TUNING.csv', sep = ',')

PandasTools.AddMoleculeColumnToFrame(df, smilesCol='SMILES', molCol='ROMol')

df_clean = df.dropna(subset=['ROMol']).copy()

mols = df_clean['ROMol'].tolist() #Listando as estruturas
labels = df_clean['CID'].astype(str).tolist() #Listando os CIDS

#Gerando a imagem em grade

img = Draw.MolsToGridImage(
	mols,
	molsPerRow = 10,
	subImgSize = (250, 250),
	legends = labels
)

img.save('QUINONAS_GRID.png')
print(f'Imagem contendo {len(mols)} quinonas criada em forma de GRID')
