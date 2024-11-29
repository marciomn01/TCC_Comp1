""" Trabalho de conclusão de curso - Computação I - EL1 -  Márcio Melchiades Nascimento """

# Data de entrega: 29/11/2024

# Importação da biblioteca random, sys, time e os

import os
import random
import time
import sys

# Regras do jogo em um dicionário
REGRAS = {
    "Tesoura": ["Papel", "Lagarto"],
    "Papel": ["Pedra", "Spok"],
    "Pedra": ["Tesoura", "Lagarto"],
    "Lagarto": ["Spok", "Papel"],
    "Spok": ["Tesoura", "Pedra"]
}

OPCOES = list(REGRAS.keys())

# Falas icônicas
FALAS = {
    ("Tesoura", "Papel"): "Tesoura corta Papel!",
    ("Papel", "Pedra"): "Papel cobre Pedra!",
    ("Pedra", "Lagarto"): "Pedra esmaga Lagarto!",
    ("Lagarto", "Spok"): "Lagarto envenena Spok!",
    ("Spok", "Tesoura"): "Spok amassa Tesoura!",
    ("Tesoura", "Lagarto"): "Tesoura degola Lagarto!",
    ("Lagarto", "Papel"): "Lagarto come Papel!",
    ("Papel", "Spok"): "Papel refuta Spok!",
    ("Spok", "Pedra"): "Spok vaporiza Pedra!",
    ("Pedra", "Tesoura"): "E como sempre foi: Pedra esmaga Tesoura!"
}

def limpar_tela():
    """Limpa o terminal para exibir apenas o necessário."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Função do menu principal
def menu():
    """
    Exibe o menu principal e retorna o estado do jogo.
    """
    limpar_tela()
    print("\n=== Bem-vindo ao The Big Bang JoKenPo! ===\n")
    print("1 - Jogar")
    print("2 - Créditos")
    print("3 - Regras")
    print("4 - Sair\n")
    
    escolha = input("Escolha uma opção: ")
    
    if escolha == "1":
        return "play"
    elif escolha == "2":
        return "credits"
    elif escolha == "3":
        return "rules"
    elif escolha == "4":
        print("\nObrigado por jogar! Até a próxima!")
        sys.exit()
    else:
        print("\nOpção inválida. Tente novamente.")
        time.sleep(1)
        return "menu"

# Função para determinar o vencedor
def determinar_vencedor(jogador, npc):
    """
    Determina o vencedor com base nas regras.
    """
    if npc in REGRAS[jogador]:
        return "jogador"
    elif jogador in REGRAS[npc]:
        return "npc"
    else:
        return "empate"

# Função principal do jogo
def jogar():
    """
    Executa o loop principal do jogo.
    """
    limpar_tela()
    print("\nQue comece a batalha épica de Pedra, Papel, Tesoura, Lagarto e Spok!\n")
    
    vitorias_jogador = 0
    vitorias_npc = 0
    empates = 0
    
    while True:
        # Limpar a tela para cada rodada
        limpar_tela()
        print(f"\nPlacar: Jogador {vitorias_jogador} x {vitorias_npc} NPC | Empates: {empates}\n")
        
        # Jogador escolhe
        print("Escolha sua jogada:")
        for i, opcao in enumerate(OPCOES, start=1):
            print(f"{i} - {opcao}")
        
        while True:
            try:
                escolha_jogador = OPCOES[int(input("\nDigite o número da sua escolha: ")) - 1]
                break
            except (ValueError, IndexError):
                print("\nEscolha inválida. Tente novamente.")

        # NPC escolhe
        escolha_npc = random.choice(OPCOES)
        print("\nJO...")
        time.sleep(0.5)
        print("KEN...")
        time.sleep(0.5)
        print("PO!\n")
        time.sleep(0.5)

        # Mostrar escolhas
        print(f"Jogador escolheu: {escolha_jogador}")
        print(f"NPC escolheu: {escolha_npc}\n")

        # Determinar o vencedor
        resultado = determinar_vencedor(escolha_jogador, escolha_npc)
        
        if resultado == "jogador":
            mensagem_vitoria = FALAS.get((escolha_jogador, escolha_npc), "Você venceu!")
            print(f"{mensagem_vitoria}\n")
            vitorias_jogador += 1
        elif resultado == "npc":
            mensagem_derrota = FALAS.get((escolha_npc, escolha_jogador), "Você perdeu!")
            print(f"{mensagem_derrota} O NPC venceu essa!\n")
            vitorias_npc += 1
        else:
            print("Empate! Que confronto acirrado!\n")
            empates += 1

        # Perguntar se o jogador está pronto para a próxima rodada
        input("Pressione Enter para continuar para a próxima rodada...")

        # Verificar se alguém venceu a melhor de 5
        if vitorias_jogador == 3:
            print("\nBazinga! Você é o grande campeão!\n")
            break
        elif vitorias_npc == 3:
            print("\nDor! A máquina venceu...\n")
            break

    # Perguntar se deseja jogar novamente
    jogar_novamente = input("\nDeseja jogar novamente? (S/N): ").strip().upper()
    if jogar_novamente != "S":
        print("\nVoltando ao menu principal...")
        time.sleep(1)

# Função para exibir os créditos
def creditos():
    limpar_tela()
    print("\n=== Créditos ===\n")
    print("Criado por: Márcio Melchiades Nascimento")
    print("Contato: marciomelchiades.20221@poli.ufrj.br")
    print("GitHub: https://github.com/marciomn01")
    print("LinkedIn: https://www.linkedin.com/in/marciomelchiadesnascimento/\n")
    input("Pressione Enter para voltar ao menu...")

# Função para exibir as regras
def regras():
    limpar_tela()
    print("\n=== Regras ===\n")
    for vencedor, derrotados in REGRAS.items():
        for derrotado in derrotados:
            print(f"{vencedor} vence {derrotado}.")
    print()
    input("Pressione Enter para voltar ao menu...")

# Função principal
def main():
    estado = "menu"
    
    while True:
        if estado == "menu":
            estado = menu()
        elif estado == "play":
            jogar()
            estado = "menu"
        elif estado == "credits":
            creditos()
            estado = "menu"
        elif estado == "rules":
            regras()
            estado = "menu"

# Executar o jogo
if __name__ == "__main__":
    main()
