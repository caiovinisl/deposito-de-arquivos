import socket
import threading

HOST = "localhost"
PORT = 8081

# Criação do socket para comunicação TCP/IP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []  # Lista de clientes conectados
ids = []  # Lista de identificadores dos clientes

servers = []  # Lista de servidores conectados
serversNames = []  # Lista de nomes dos servidores


def globalMessage(message):
    # Envio da mensagem para todos os servidores conectados
    for server in servers:
        try:
            server.send(message)
        except:
            print("Erro ao enviar mensagem para um servidor")


def globalM(message):
    # Envio da mensagem para todos os clientes conectados
    for client in clients:
        try:
            client.send(message)
        except:
            print("Erro ao enviar mensagem para um cliente")


def handleMessages(client, agent):
    while True:
        try:
            if agent == "client":
                # Recebimento de mensagem do cliente
                receiveMessageFromClient = client.recv(1024).decode()
                print("receiveMessageFromClient")
                print(receiveMessageFromClient)
                globalMessage(f"{receiveMessageFromClient}".encode())
            elif agent == "server":
                # Recebimento de mensagem do servidor
                receiveMessageFromClient = client.recv(1024).decode()
                print("receiveMessageFromClient")
                print(receiveMessageFromClient)
                globalM(f"{receiveMessageFromClient}".encode())
        except:
            client.close()
            print("Erro ao lidar com as mensagens do cliente ou servidor")


def initialConnection():
    print("Proxy inicializado. Aguardando conexões...")
    while True:
        try:
            client, address = server.accept()
            print(f"Nova conexão: {str(address)}")

            # Envio da identificação do agente (cliente ou servidor)
            client.send("agent".encode())
            agent = client.recv(1024).decode()

            if agent == "client":
                # Adiciona o cliente à lista de clientes conectados
                clients.append(client)
                ids.append(agent)
                # Cria uma thread para lidar com as mensagens do cliente
                user_thread = threading.Thread(
                    target=handleMessages,
                    args=(
                        client,
                        agent,
                    ),
                )
                user_thread.start()
                print("Cliente conectado")
            else:
                # Adiciona o servidor à lista de servidores conectados
                servers.append(client)
                serversNames.append(agent)
                # Cria uma thread para lidar com as mensagens do servidor
                user_thread = threading.Thread(
                    target=handleMessages,
                    args=(
                        client,
                        agent,
                    ),
                )
                user_thread.start()
                print("Servidor conectado")
        except:
            print("Erro ao aceitar conexão")
            pass


try:
    initialConnection()
except:
    print("Erro ao iniciar a conexão")
    quit()
