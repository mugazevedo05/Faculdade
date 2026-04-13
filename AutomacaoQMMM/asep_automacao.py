import os
import subprocess
import MDAnalysis as mda
import numpy as np

# =============================================================================
# ETAPA 1: TRATAMENTO DA TRAJETÓRIA COM GROMACS
# =============================================================================

def tratar_trajetoria_gromacs(tpr_file, xtc_file, output_fit):
    """
    Função responsável por pegar a dinâmica bruta do GROMACS e transformá-la 
    no 'filme final' onde a benzoquinona fica congelada no centro da caixa.
    """
    print("\n--- Iniciando o processamento da trajetória no GROMACS ---")
    
    # Passo 1.1: Corrigir as moléculas de água cortadas pelas bordas (PBC whole)
    # Isso garante que nenhuma molécula seja lida pela metade.
    print("Corrigindo as condições periódicas de contorno (PBC whole)...")
    cmd_whole = f"gmx trjconv -s {tpr_file} -f {xtc_file} -o traj_whole.xtc -pbc whole"
    # O input b"0\n" simula o usuário digitando "0" (System) e apertando Enter
    subprocess.run(cmd_whole, shell=True, input=b"0\n", check=True, stdout=subprocess.DEVNULL)

    # Passo 1.2: Centralizar a benzoquinona no meio da caixa
    print("Centralizando a benzoquinona...")
    cmd_center = f"gmx trjconv -s {tpr_file} -f traj_whole.xtc -o traj_center.xtc -pbc mol -center"
    # O input b"1\n0\n" seleciona "1" (supondo que 1 seja a sua molécula) para centrar, e "0" (System) para salvar
    subprocess.run(cmd_center, shell=True, input=b"1\n0\n", check=True, stdout=subprocess.DEVNULL)

    # Passo 1.3: Fazer o Fit Rotacional e Translacional (Congelar a quinona)
    print("Realizando o fit estrutural (congelando a molécula)...")
    cmd_fit = f"gmx trjconv -s {tpr_file} -f traj_center.xtc -o {output_fit} -fit rot+trans"
    # Seleciona "1" para o Fit, e "0" para salvar
    subprocess.run(cmd_fit, shell=True, input=b"1\n0\n", check=True, stdout=subprocess.DEVNULL)
    
    # Passo 1.4: Faxina
    # Apagamos os arquivos intermediários gigantes para não lotar o seu HD
    print("Limpando arquivos temporários...")
    os.remove("traj_whole.xtc")
    os.remove("traj_center.xtc")
    
    print(f"Sucesso! Trajetória final salva como: {output_fit}\n")

# =============================================================================
# ETAPA 2: EXTRAÇÃO DO CAMPO MÉDIO (MDAnalysis + NumPy)
# =============================================================================

def extrair_campo_medio(tpr_file, traj_fit_file, pc_output, carga_O=-0.834, carga_H=0.417, num_frames=100):
    """
    Lê a trajetória congelada, extrai a rede de solvente de 100 quadros,
    divide as cargas e gera o arquivo .pc para o ORCA.
    """
    print("\n--- Iniciando a extração do campo elétrico do solvente ---")
    
    # Passo 2.1: Carregar o "Universo"
    print("Carregando topologia e trajetória na memória...")
    u = mda.Universe(tpr_file, traj_fit_file)
    
    # Passo 2.2: A Seleção Cirúrgica
    # Selecionamos apenas os átomos de oxigênio (OW) e hidrogênio (HW1, HW2) da água (SOL)
    print("Selecionando moléculas de água...")
    oxigenios = u.select_atoms("resname SOL and name OW")
    hidrogenios = u.select_atoms("resname SOL and (name HW1 or name HW2)")

    # Passo 2.3: A Matemática dos Quadros (Frames)
    # Descobrimos quantos quadros tem no filme todo e calculamos o "salto" 
    # para garantir que pegaremos as 100 fotos bem espaçadas umas das outras.
    total_frames = len(u.trajectory)
    step = max(1, total_frames // num_frames)
    print(f"Total de quadros no filme: {total_frames}. Extraindo 1 foto a cada {step} quadros.")
    
    # Preparamos a carga fracionária (dividida por 100)
    carga_frac_O = carga_O / num_frames
    carga_frac_H = carga_H / num_frames
    
    # Lista que vai guardar as linhas de texto do arquivo final
    linhas_pc = []
    frames_coletados = 0
    
    # Passo 2.4: O Loop de Captura
    for ts in u.trajectory[::step]:
        if frames_coletados >= num_frames:
            break # Para o loop se já pegou as 100 fotos
            
        # Pega as coordenadas (X, Y, Z) exatas dos átomos neste quadro
        # Multiplicamos por 10 porque o MDAnalysis lê em Angstroms, e o ORCA precisa disso em Angstroms (MDAnalysis nativamente usa Angstrom, GROMACS usa nm, então aqui já está correto).
        pos_O = oxigenios.positions 
        pos_H = hidrogenios.positions 
        
        # Formata os dados no padrão do ORCA: [Carga] [X] [Y] [Z]
        for coord in pos_O:
            linhas_pc.append(f"{carga_frac_O:8.5f} {coord[0]:8.3f} {coord[1]:8.3f} {coord[2]:8.3f}\n")
            
        for coord in pos_H:
            linhas_pc.append(f"{carga_frac_H:8.5f} {coord[0]:8.3f} {coord[1]:8.3f} {coord[2]:8.3f}\n")
            
        frames_coletados += 1

    print(f"Frames coletados = {frames_coletados}")

    # Passo 2.5: A Escrita do Arquivo .pc
    print(f"Escrevendo o arquivo final com {len(linhas_pc)} cargas pontuais...")
    with open(pc_output, 'w') as f:
        f.write(f"{len(linhas_pc)}\n") 
        f.writelines(linhas_pc)
        
    print(f"Sucesso! Arquivo de cargas pontuais gerado: {pc_output}\n")
    
    # NOVIDADE: Extrair as coordenadas da quinona congelada para dar para o ORCA
    quinona = u.select_atoms("resname UNL") # Substitua QUI pelo nome da sua molécula na topologia
    
    # Transforma as posições em um bloco de texto formatado
    bloco_xyz = ""
    for atomo in quinona:
        # Pega o nome do elemento (ex: C, O, H) e as posições
        bloco_xyz += f"{atomo.element:2s} {atomo.position[0]:8.5f} {atomo.position[1]:8.5f} {atomo.position[2]:8.5f}\n"
        
    return bloco_xyz # A função agora devolve esse texto para usarmos na Etapa 3

    
# =============================================================================
# ETAPA 3: GERAÇÃO DO INPUT DO ORCA
# =============================================================================

def gerar_input_orca(inp_output, pc_file, coords_quinona, omega_val, carga=0, multiplicidade=1):
    """
    Cria o arquivo de input (.inp) do ORCA injetando as configurações do 
    usuário, o arquivo de cargas pontuais e as coordenadas congeladas.
    """
    print(f"\n--- Gerando arquivo de input do ORCA: {inp_output} ---")
    
    # Usamos f-strings (o 'f' antes das aspas) para que o Python troque 
    # as palavras entre chaves {} pelos valores reais das nossas variáveis.
    
    conteudo_orca = f"""! wB97X def2-TZVPP TIGHTSCF RIJCOSX def2/J HIRSHFELD

# Aponta para a rede de solvente que extraímos do GROMACS
%pointcharges "{pc_file}"

# Configuração do Optimal Tuning
%method
    RangeSepMu {omega_val}
end

# Coordenadas da quinona centralizada
* xyz {carga} {multiplicidade}
{coords_quinona}*
"""

    # Escreve tudo no arquivo final
    with open(inp_output, 'w') as f:
        f.write(conteudo_orca)
        
    print(f"Sucesso! Input gerado com RangeSepMu = {omega_val}")


# =============================================================================
# EXECUÇÃO PRINCIPAL (O PAINEL DE CONTROLE)
# =============================================================================

if __name__ == "__main__":
    print("=====================================================")
    print("  Automação QM/MM (ASEP) - Teste Benzoquinona")
    print("=====================================================\n")

    # 1. VARIÁVEIS DE ENTRADA (Mude os nomes dos arquivos aqui)
    # Coloque aqui os arquivos da sua dinâmica real que já rodou
    arquivo_tpr = "md.tpr"               
    arquivo_xtc = "md.xtc"               
    
    # 2. VARIÁVEIS DE SAÍDA (Como você quer chamar os novos arquivos)
    traj_fit_out = "traj_fit.xtc"        
    arquivo_pc = "solvente_medio.pc"     
    arquivo_inp = "calculo_qm.inp"       
    
    # 3. PARÂMETROS DA MOLÉCULA
    omega_otimizado = "0.250"            # Valor do RangeSepMu para essa quinona
    carga_mol = 0
    mult_mol = 1

    # =========================================================================
    # O FLUXO DE TRABALHO
    # =========================================================================
    
    try:
        # PASSO 1: Chama o GROMACS para centralizar a trajetória
        tratar_trajetoria_gromacs(arquivo_tpr, arquivo_xtc, traj_fit_out)

        # PASSO 2: Chama o MDAnalysis para extrair o solvente médio e a quinona
        xyz_texto = extrair_campo_medio(arquivo_tpr, traj_fit_out, arquivo_pc)

        # PASSO 3: Monta o arquivo do ORCA com tudo integrado
        gerar_input_orca(arquivo_inp, arquivo_pc, xyz_texto, omega_otimizado, carga_mol, mult_mol)

        print("\n>>> Pipeline de preparação concluído! O arquivo .inp está pronto para o ORCA.")
        
    except Exception as e:
        print(f"\n[ERRO] A automação parou devido a um erro: {e}")

