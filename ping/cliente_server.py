import socket
import time
import select

# Configurações do cliente
HOST = '25.18.56.223'  # Endereço IP do servidor
PORT = 65000          # Porta utilizada pelo servidor

# Cria o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor

def server_conn(HOST, PORT):
    try:
        client_socket.connect((HOST, PORT))
        
    except TimeoutError:
        print("nao foi possivel se conectar ao servidor.")
        time.sleep(5)
        print("Nova tentativa em 25s")
        server_conn(HOST, PORT)
        
server_conn(HOST, PORT)
print(f"Conectado ao servidor {HOST}:{PORT}")

# Loop infinito para manter a conexão com o servidor

while True:
    # Verifica se há dados disponíveis para leitura no socket
    ready_to_read, _, _ = select.select([client_socket], [], [], 30)

    if ready_to_read:
        # Recebe a resposta do servidor
        data = client_socket.recv(1024)

        if not data:
            # Caso não haja dados, significa que a conexão foi encerrada
            print("Conexão encerrada com o servidor")
            time.sleep(5)
            print("Tentar nova conexão em e 25s")
            server_conn(HOST, PORT)
            
        print(f"Resposta recebida: {data.decode()}")

    else:
        # Caso não haja dados disponíveis para leitura, exibe uma mensagem de verificação e tenta conectar novamente...
        print("Verificando conexão...")
        time.sleep(5)
        server_conn(HOST, PORT)
        
    # Envia uma mensagem para o servidor
    msg = "Mensagem de teste"
    client_socket.sendall(msg.encode())
