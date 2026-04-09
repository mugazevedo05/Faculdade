import pandas as pd
from sklearn.preprocessing import StandardScaler

df = 	pd.read_csv('/home/mugazevedo05/MOLECULAS/CID_n_otm/SMILES/RDKIT/DADOS/QUINONAS_DESCRITORES.csv', sep=',')

df_limpo = df.dropna().reset_index(drop=True)

col_texto = ['SMILES', 'CID']
col_descritores = [col for col in df_limpo.columns if col not in col_texto]

X = df_limpo[col_descritores]

scaler = StandardScaler()

x_padrao = scaler.fit_transform(X)

df_padronizado = pd.DataFrame(x_padrao, columns = col_descritores)

df_ml = pd.concat([df_limpo[col_texto], df_padronizado], axis = 1)

print("Dados padronizados em QUINONAS_DESCRITORES")

df_ml.to_csv('QUINONAS_DESCRITORES_P.csv', index=False)
