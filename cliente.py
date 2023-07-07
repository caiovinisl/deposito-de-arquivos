import socket
import threading
import os
import uuid

HOST = "localhost"
PORT = 8081

agent = "client"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def debug_print(message):
  print(f"[debug] | [{message}]")


def receiveMessage():
  while True:
    if client.fileno() == -1:
      break
    try:
      message = client.recv(1024).decode()
      if message == "agent":
        client.send(agent.encode())
      elif message == 'file':
        print(f"saving file... {message}")
      else:
        print(f"message: {message}")
    except:
      print('Exit')

def send_recover_message(file_name,client_id,level, file_size):
  chunk = "2"+"|"+file_name+"|"+str(level)+"|"+str(file_size)
  client.send(chunk.encode())

def send_deposit_message(file_name,client_id,level, file_size):
  chunk = "1"+"|"+file_name+"|"+str(level)+"|"+str(file_size)+"|"
  client.send(chunk.encode())
  
  path = os.path.dirname(__file__)
  file_path = os.path.join(path, file_name)
  
  with open(file_path, "rb") as file:
    while True:
      data = file.read(1024)
      debug_print('sending file chunk')
      if not data:
        break
      client.send(data)


client_id = str(uuid.uuid4())


def startup_menu():
  while True:
    print("Menu:")
    print("1. Depositar arquivo")
    print("2. Recuperar arquivo")
    print("3. Sair")
    choice = int(input())

    if choice == 1:
      file_name = input("Nome do arquivo: ")
      level = int(input("Número de cópias: "))

      path = os.path.dirname(__file__)
      file_path = os.path.join(path, file_name)
      file_size = os.path.getsize(file_path)
      
      receiver_thread = threading.Thread(target=receiveMessage,args=()) 
      sender_thread = threading.Thread(target=send_deposit_message,args=(file_name,client_id,level, file_size))

      receiver_thread.start()
      sender_thread.start()
      receiver_thread.join(0.5)
      sender_thread.join(0.5)
    if choice == 2:
      file_name = input("Nome do arquivo: ")
      
      receiver_thread = threading.Thread(target=receiveMessage,args=()) 
      sender_thread = threading.Thread(target=send_recover_message,args=(file_name,client_id, 0, 0))

      receiver_thread.start()
      sender_thread.start()
      receiver_thread.join(0.5)
      sender_thread.join(0.5)
    if choice ==  3:
      client.close()
      break
    if choice not in (1,2,3):
      print(f'Operação não encontrada')


def main():
  try:
    client.connect((HOST,PORT))
    print(f'Conectado ao host com sucesso!')
    debug_print(f"host connected: ({HOST}:{PORT})")
    startup_menu()
  except:
    client.close()

if __name__ == "__main__":
  main()
