import socket


# Configurações do servidor
HOST = '26.18.56.223' # Endereço IP do servidor
PORT = 65000     # Porta utilizada pelo servidor

# Cria o socket do servidor
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configura o servidor para ficar esperando por conexões
serv_socket.bind((HOST, PORT))
serv_socket.listen()

print(f"Servidor esperando por conexões em {HOST}:{PORT}")

# Dicionário para armazenar as mensagens recebidas de cada cliente
clients_msgs = {}

while True:
    # Aceita uma nova conexão
    client_socket, addr = serv_socket.accept()

    print(f"Conexão estabelecida com {addr}")

    # Adiciona o socket do cliente ao dicionário de mensagens
    clients_msgs[client_socket] = []

    # Loop para receber mensagens do cliente
    while True:
        # Recebe uma mensagem do cliente
        data = client_socket.recv(1024) # ConnectionResetError

        # Verifica se o cliente encerrou a conexão
        if not data:
            print(f"Conexão com {addr} encerrada")
            break

        # Adiciona a mensagem recebida ao dicionário de mensagens
        clients_msgs[client_socket].append(data.decode())

        # Envia uma resposta para o cliente
        msg = "Mensagem recebida"
        client_socket.sendall(msg.encode())

    # Fecha a conexão com o cliente
    client_socket.close()

# Fecha o socket do servidor
