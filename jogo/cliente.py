import socket

# Configuração do cliente
HOST = 'localhost'
PORT = 5000

# Conexão com o servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Loop principal do jogo
while True:
    letra = input("Digite uma letra: ").lower()

    # Envio da letra ao servidor
    sock.sendall(letra.encode())

    # Recebimento da resposta do servidor
    data = sock.recv(1024).decode()
    print(data)
    if "Você perdeu" in data or "Parabéns" in data:
        resposta = input("Quer jogar novamente?(S/N): ")
        sock.sendall(resposta.encode())
        
        if resposta.lower() == "n":
            # Fechamento da conexão
            sock.close()
            break
