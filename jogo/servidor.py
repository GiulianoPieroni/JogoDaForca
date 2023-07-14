import socket
import random

# Lista de palavras
palavras = ["ifmg", "programacao", "finalboss", "forca", "jorge", "racionais"]

# Dicionário para armazenar as estatísticas dos clientes
estatisticas_clientes = {}

# Chances de Erro
chances = 5

# Tentativas do usuário
letras_usuario = []

# Validação de vitória
ganhou = False 

# Função para escolher aleatoriamente uma palavra da lista
def escolher_palavra():
    return random.choice(palavras).lower()

# Escolha de uma nova palavra
palavra_escolhida = escolher_palavra()

# Função para processar a letra enviada pelo cliente
def processar_letra(letra):
    global chances, letras_usuario, ganhou

    # Verificar se a letra já foi fornecida pelo usuário
    if letra.lower() in letras_usuario:
        return "Letra repetida."

    letras_usuario.append(letra.lower())

    if letra.lower() not in palavra_escolhida.lower():
        chances -= 1

    # Verificar se o jogador ganhou
    ganhou = True
    for letra_palavra in palavra_escolhida:
        if letra_palavra.lower() not in letras_usuario:
            ganhou = False
            break

    if ganhou:
        letras_usuario.clear()
        return f"Parabéns, você ganhou! A palavra era: {palavra_escolhida}"
    elif chances == 0:
        letras_usuario.clear()
        return f"Você perdeu! A palavra era: {palavra_escolhida}"
    else:
        # Montar a palavra atual com as letras corretas adivinhadas
        palavra_atual = ""
        for letra_palavra in palavra_escolhida:
            if letra_palavra.lower() in letras_usuario:
                palavra_atual += letra_palavra + " "
            else:
                palavra_atual += "_ "

        return f"{palavra_atual}\nVocê tem {chances} chances restantes."


# Configuração do servidor
HOST = 'localhost'
PORT = 5000

# Criação do socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

print("Aguardando conexão do cliente...")

while True:
    # Aceitação da conexão do cliente
    conn, addr = sock.accept()
    print("Conexão estabelecida com", addr)

    # Armazena o IP do cliente
    ip_cliente = addr[0]

    # Verifica se é um cliente novo
    if ip_cliente not in estatisticas_clientes:
        estatisticas_clientes[ip_cliente] = [0, 0]  # [Vitórias, Derrotas]

    # Escolha de uma nova palavra
    palavra_escolhida = escolher_palavra()

    # Reinicialização das variáveis para um novo jogo
    tentativas_erradas = 0
    letras_adivinhadas = []
    chances = 5
    ganhou = False

    # Loop principal do jogo
    while True:
    # Recebimento da letra enviada pelo cliente
        letra = conn.recv(1024).decode().strip()

        # Processamento da letra e obtenção da resposta
        resposta = processar_letra(letra)

        # Envio da resposta para o cliente
        conn.send(resposta.encode())
    
        # Verificação do fim do jogo
        if chances == 0 or ganhou:
            # Atualiza as estatísticas do cliente
            if ganhou:
                estatisticas_clientes[ip_cliente][0] += 1  # Incrementa as vitórias
            else:
                estatisticas_clientes[ip_cliente][1] += 1  # Incrementa as derrotas
            # Envio da pergunta sobre jogar novamente
            resposta = conn.recv(1024).decode().strip()
            
            print("   IP | Vitorias: | Derrotas: ")
            print(estatisticas_clientes)

            if resposta.lower() == "s":
                # Escolha de uma nova palavra
                palavra_escolhida = escolher_palavra()

                # Reinicialização das variáveis para um novo jogo
                tentativas_erradas = 0
                letras_adivinhadas.clear()
                chances = 5
                ganhou = False
            else:
                break

    # Fechamento da conexão com o cliente
    conn.close()
    print("Conexão fechada com", addr)

