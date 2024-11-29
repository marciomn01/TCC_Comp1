""" Trabalho de conclusão de curso - Computação I - EL1 -  Márcio Melchiades Nascimento """

# Data de entrega: 29/11/2024

# Importação da biblioteca random, sys, time e os

import os
import random
import sys
import time

# Configurações do jogo
TAMANHO_TABULEIRO = 10
NAVIOS_TAMANHOS = [5, 4, 3, 3, 1]

def limpar_tela():
    """Limpa o terminal para melhorar a visualização."""
    os.system('cls' if os.name == 'nt' else 'clear')

def criar_tabuleiro():
    """Cria um tabuleiro vazio."""
    return [["~"] * TAMANHO_TABULEIRO for _ in range(TAMANHO_TABULEIRO)]

def mostrar_tabuleiro(tabuleiro, ocultar_navios=False):
    """Exibe o tabuleiro no terminal."""
    for linha in tabuleiro:
        print(" ".join("~" if (ocultar_navios and celula == "N") else celula for celula in linha))
    print()

def pode_colocar_navio(tabuleiro, linha, coluna, tamanho, orientacao):
    """Verifica se é possível colocar o navio em uma posição."""
    if orientacao == "H":
        if coluna + tamanho > TAMANHO_TABULEIRO:
            return False
        return all(tabuleiro[linha][coluna + i] == "~" for i in range(tamanho))
    elif orientacao == "V":
        if linha + tamanho > TAMANHO_TABULEIRO:
            return False
        return all(tabuleiro[linha + i][coluna] == "~" for i in range(tamanho))

def colocar_navio(tabuleiro, linha, coluna, tamanho, orientacao):
    """Coloca um navio no tabuleiro."""
    if orientacao == "H":
        for i in range(tamanho):
            tabuleiro[linha][coluna + i] = "N"
    elif orientacao == "V":
        for i in range(tamanho):
            tabuleiro[linha + i][coluna] = "N"

def remover_navio(tabuleiro, linha, coluna, tamanho, orientacao):
    """Remove um navio do tabuleiro."""
    if orientacao == "H":
        for i in range(tamanho):
            tabuleiro[linha][coluna + i] = "~"
    elif orientacao == "V":
        for i in range(tamanho):
            tabuleiro[linha + i][coluna] = "~"

def atacar(tabuleiro, linha, coluna):
    """Realiza um ataque no tabuleiro."""
    if tabuleiro[linha][coluna] == "N":
        tabuleiro[linha][coluna] = "X"
        return True
    elif tabuleiro[linha][coluna] == "~":
        tabuleiro[linha][coluna] = "O"
    return False

def checar_vitoria(tabuleiro):
    """Verifica se todos os navios de um tabuleiro foram destruídos."""
    for linha in tabuleiro:
        if "N" in linha:
            return False
    return True

def solicitar_coordenadas(mensagem, limite, tabuleiro=None):
    """Solicita coordenadas válidas do jogador."""
    while True:
        try:
            entrada = input(mensagem)
            linha, coluna = map(int, entrada.split())
            if 0 <= linha < limite and 0 <= coluna < limite:
                if tabuleiro and tabuleiro[linha][coluna] in ["O", "X"]:
                    print("\nVocê já atacou essa posição! Escolha outra.\n")
                else:
                    return linha, coluna
            else:
                print(f"\nCoordenadas fora do limite! Certifique-se de usar valores entre 0 e {limite - 1}.\n")
        except ValueError:
            print("\nEntrada inválida! Digite duas coordenadas separadas por espaço.\n")

def escolher_coordenadas_npc(tabuleiro):
    """Escolhe coordenadas aleatórias para o NPC atacar."""
    while True:
        linha = random.randint(0, TAMANHO_TABULEIRO - 1)
        coluna = random.randint(0, TAMANHO_TABULEIRO - 1)
        if tabuleiro[linha][coluna] not in ["O", "X"]:
            return linha, coluna

def jogar():
    """Executa o loop principal do jogo."""
    limpar_tela()
    print("=== Batalha Naval ===\n")
    print("Posicione seus navios e destrua o inimigo!\n")
    
    jogador_tabuleiro = criar_tabuleiro()
    npc_tabuleiro = criar_tabuleiro()

    # NPC posiciona navios automaticamente
    for tamanho in NAVIOS_TAMANHOS:
        while True:
            linha = random.randint(0, TAMANHO_TABULEIRO - 1)
            coluna = random.randint(0, TAMANHO_TABULEIRO - 1)
            orientacao = random.choice(["H", "V"])
            if pode_colocar_navio(npc_tabuleiro, linha, coluna, tamanho, orientacao):
                colocar_navio(npc_tabuleiro, linha, coluna, tamanho, orientacao)
                break

    # Posicionamento do jogador
    print("Seu tabuleiro vazio:\n")
    mostrar_tabuleiro(jogador_tabuleiro)

    for tamanho in NAVIOS_TAMANHOS:
        while True:
            print(f"\nPosicione um navio de tamanho {tamanho}:\n")
            linha, coluna = solicitar_coordenadas(f"Digite a linha e a coluna iniciais (0 a {TAMANHO_TABULEIRO - 1}, separados por espaço): ", TAMANHO_TABULEIRO)
            orientacao = input("Digite a orientação (H para horizontal, V para vertical): ").strip().upper()

            if orientacao not in ["H", "V"]:
                print("\nOrientação inválida! Tente novamente.\n")
                continue

            if pode_colocar_navio(jogador_tabuleiro, linha, coluna, tamanho, orientacao):
                colocar_navio(jogador_tabuleiro, linha, coluna, tamanho, orientacao)
                limpar_tela()
                print("Seu tabuleiro atualizado:\n")
                mostrar_tabuleiro(jogador_tabuleiro)

                # Perguntar se deseja reposicionar o navio
                reposicionar = input("Deseja remover este navio e reposicioná-lo? (S/N): ").strip().upper()
                if reposicionar == "S":
                    remover_navio(jogador_tabuleiro, linha, coluna, tamanho, orientacao)
                    print("\nNavio removido. Reposicione-o!\n")
                else:
                    break
            else:
                print("\nNão é possível posicionar o navio nessa posição. Tente novamente.\n")

    # Loop do jogo
    while True:
        limpar_tela()
        print("=== Seu Tabuleiro ===\n")
        mostrar_tabuleiro(jogador_tabuleiro)
        print("=== Tabuleiro do NPC ===\n")
        mostrar_tabuleiro(npc_tabuleiro, ocultar_navios=True)

        # Turno do jogador
        print("\nSeu turno:\n")
        linha, coluna = solicitar_coordenadas(f"Digite as coordenadas de ataque (linha e coluna, 0 a {TAMANHO_TABULEIRO - 1}): ", TAMANHO_TABULEIRO, npc_tabuleiro)
        acertou = atacar(npc_tabuleiro, linha, coluna)
        print("\nVocê acertou!" if acertou else "\nVocê errou!")
        time.sleep(1)

        if checar_vitoria(npc_tabuleiro):
            print("\nParabéns! Você venceu!\n")
            break

        # Turno do NPC
        print("\nTurno do NPC...\n")
        time.sleep(1)
        linha, coluna = escolher_coordenadas_npc(jogador_tabuleiro)
        acertou = atacar(jogador_tabuleiro, linha, coluna)
        print(f"NPC atacou em ({linha}, {coluna}) e {'acertou!' if acertou else 'errou!'}\n")
        time.sleep(1)

        if checar_vitoria(jogador_tabuleiro):
            print("\nVocê perdeu! Tente novamente.\n")
            break

def regras():
    """Exibe as regras do jogo."""
    limpar_tela()
    print("=== Regras da Batalha Naval ===\n")
    print("1. Cada jogador posiciona seus navios no tabuleiro (horizontal ou vertical).")
    print("2. O objetivo é destruir todos os navios do oponente.")
    print("3. Durante o turno, escolha uma coordenada para atacar.")
    print("4. O jogo termina quando todos os navios de um jogador forem destruídos.\n")
    input("Pressione Enter para voltar ao menu...")

def creditos():
    """Exibe os créditos do jogo."""
    limpar_tela()
    print("=== Créditos ===\n")
    print("Criado por: Márcio Melchiades Nascimento")
    print("Contato: marciomelchiades.20221@poli.ufrj.br")
    print("GitHub: https://github.com/marciomn01")
    print("LinkedIn: https://www.linkedin.com/in/marciomelchiadesnascimento/\n")
    input("Pressione Enter para voltar ao menu...")

def menu():
    """Exibe o menu principal."""
    while True:
        limpar_tela()
        print("=== Bem-vindo ao Menu Principal do Batalha Naval! ===\n")
        print("1 - Jogar")
        print("2 - Regras")
        print("3 - Créditos")
        print("4 - Sair\n")
        
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            jogar()
        elif escolha == "2":
            regras()
        elif escolha == "3":
            creditos()
        elif escolha == "4":
            print("\nObrigado por jogar! Até a próxima!")
            sys.exit()
        else:
            print("\nOpção inválida! Tente novamente.\n")
            time.sleep(1)

# Executa o menu principal
if __name__ == "__main__":
    menu()
