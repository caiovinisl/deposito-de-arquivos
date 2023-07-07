import socket
import threading

HOST = "localhost"
PORT = 8081

# Cria o socket do servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

# Lista de clientes conectados
clientes = []
ids = []

# Lista de servidores conectados
servidores = []
nomes_servidores = []

def mensagem_global(message, agent):
  if agent == 'server':
    txt = servidores[-1]
  else:
    txt = clientes[-1]
  txt.send(message)

# Função para lidar com as mensagens recebidas dos clientes e servidores
def lidar_com_mensagens(client, agent):
  while True:
    try:
      if agent == "client":
        # Recebe mensagem do cliente
        receber_mensagem_do_cliente = client.recv(1024).decode()
        print("receber_mensagem_do_cliente")
        print(receber_mensagem_do_cliente)
        # Envia mensagem para todos os servidores
        mensagem_global(f'{receber_mensagem_do_cliente}'.encode(), 'server')
      elif agent == "server":
        # Recebe mensagem do servidor
        receber_mensagem_do_cliente = client.recv(1024).decode()
        print("receber_mensagem_do_cliente")
        print(receber_mensagem_do_cliente)
        # Envia mensagem para todos os clientes
        mensagem_global(f'{receber_mensagem_do_cliente}'.encode(), 'client')
    except:
      client.close()

# Função para estabelecer a conexão inicial com os clientes e servidores
def conexao_inicial():
  while True:
    try:
      # Aceita a conexão de um cliente
      cliente, endereco = servidor.accept()
      print(f"Nova Conexão: {str(endereco)}")

      cliente.send('agent'.encode())
      agente = cliente.recv(1024).decode()

      if agente == "client":
        # Adiciona o cliente à lista de clientes
        clientes.append(cliente)
        ids.append(agente)
        # Inicia uma thread para lidar com as mensagens do cliente
        thread_usuario = threading.Thread(target=lidar_com_mensagens, args=(cliente, agente,))
        thread_usuario.start()
      else:
        # Adiciona o servidor à lista de servidores
        servidores.append(cliente)
        nomes_servidores.append(agente)
        # Inicia uma thread para lidar com as mensagens do servidor
        thread_usuario = threading.Thread(target=lidar_com_mensagens, args=(cliente, agente,))
        thread_usuario.start()
    except:
      quit()


try:
  conexao_inicial()
except:
  print('Erro ao iniciar conexão')
  quit()
