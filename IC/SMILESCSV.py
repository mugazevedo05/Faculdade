import pandas as pd
from rdkit.Chem import PandasTools

# 1. Vamos ler o arquivo manualmente para ter controle total
dados = []
with open('/home/mugazevedo05/MOLECULAS/CID_n_otm/SMILES/RDKIT/DADOS/SMILES_TUNING.csv', 'r') as f:
    linhas = f.readlines()

# 2. Limpar e separar cada linha
for linha in linhas:
    # .split() sem argumentos divide a string por qualquer quantidade de espaços ou tabs
    partes = linha.split() 

    # Se a linha não estiver vazia
    if len(partes) >= 2:
        # A primeira parte é sempre o SMILES
        smiles = partes[0] 
        # Junta o que sobrou para formar o nome (ex: "CID", "12345")
        nome_cid = " ".join(partes[2:3]) 

        dados.append({'SMILES': smiles, 'CID': nome_cid})

# 3. Transforma na tabela do Pandas
df = pd.DataFrame(dados)
df.to_csv('SMILES_TUNING.csv')

print(f"Total de quinonas processadas com sucesso: {len(df)}")
