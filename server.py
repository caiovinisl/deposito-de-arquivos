import socket
import threading
import shutil
import os

# Configurações do servidor
HOST = "localhost"
PORT = 8081

# Criação do socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Identificador do agente (servidor)
agent = "server"

# Lista para armazenar os nomes dos arquivos recebidos
files = []

# Função para imprimir mensagens de depuração
def debug_print(message):
  print(f"[debug] | [{message}]")

try:
  # Conecta ao servidor
  client.connect((HOST, PORT))
  print(f'Conexão estabelecida com sucesso em {HOST}:{PORT}')
except:
  print(f'ERRO: Verifique o host')

def split_message(chunk):
  array = chunk.split('|')
  return array

# Função para receber mensagens no servidor
def receive_message():
  while True:
    try:
      message = client.recv(1024).decode()
      debug_print(f"message: {message}")

      # Verifica se a mensagem é uma solicitação para identificar o agente
      if message == 'agent':
        client.send(agent.encode())
      else:
        # Divide a mensagem recebida em partes
        message = split_message(message)
        choice = int(message[0])  # Opção escolhida
        file_name = message[1]   # Nome do arquivo
        level = int(message[2])  # Nível de replicação
        file_size = int(message[3])  # Tamanho do arquivo

        print("Operação iniciada: " + str(choice))
        debug_print(str(message))

        if choice == 1:
          client.send("Recebendo arquivo...".encode())

          # Adiciona o nome do arquivo à lista de arquivos recebidos
          files.append(file_name)

          # Obtém o caminho do diretório atual
          path = os.path.dirname(__file__)

          # Constrói o caminho completo do arquivo a ser salvo
          file_path = os.path.join(path, "data", file_name)

          with open(file_path, "wb") as file:
            count = 0
            while count <= (file_size / 1024):
              debug_print('recebendo fragmento de arquivo')
              file_chunk = client.recv(1024)
              file.write(file_chunk)
              count += 1

          # Envia uma mensagem de confirmação
          output = file_name + ' salvo com sucesso'
          client.send(output.encode())

          # Se o nível de replicação for maior que 0, cria réplicas do arquivo
          if level > 0:
            for i in range(level):
              dest_path = file_path + f".replica-{i + 1}"
              shutil.copy(file_path, dest_path)

            # Envia uma mensagem indicando a criação das réplicas
            output = str(level) + ' Réplicas criadas com sucesso'
            client.send(output.encode())

        elif choice == 2:
          client.send("Buscando arquivo...".encode())

          # Verifica se o arquivo solicitado está na lista de arquivos recebidos
          if file_name not in files:
            client.send((file_name + ' não encontrado').encode())
            continue

          # Envia uma mensagem indicando que o arquivo foi encontrado
          output = file_name + " encontrado com sucesso"
          client.send(output.encode())

          # Envia uma mensagem indicando que a restauração do arquivo está em andamento
          client.send("Restaurando...".encode())

          with open(file_path, "rb") as file:
            while True:
              data = file.read(1024)
              debug_print('enviando fragmento de arquivo')
              if not data:
                break

              client.send(data)

          # Envia uma mensagem indicando que a restauração do arquivo foi concluída
          client.send("Arquivo Restaurado!".encode())

    except:
      print('[ERRO]')
      quit()

receive_message()
