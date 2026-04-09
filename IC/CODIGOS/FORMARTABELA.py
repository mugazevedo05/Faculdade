import pandas as pd
import dataframe_image as dfi

df_final = pd.read_csv('/home/mugazevedo05/MOLECULAS/CID_n_otm/SMILES/RDKIT/DADOS/QUINONAS_DESCRITORES_P.csv', sep = ',')

df_amostra = df_final.head(10)

print('Gerando imagens: QUINONAS_DESCRITORES.png e QUINONAS_DESCRITORES_AMOSTRAL.png')
dfi.export(df_final, 'QUINONAS_DESCRITORES_P.png', max_rows = -1, table_conversion='matplotlib')
dfi.export(df_amostra, 'QUINONAS_DESCRITORES_AMOSTRAL_P.png', table_conversion='matplotlib')
