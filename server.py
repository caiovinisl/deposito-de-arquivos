import socket
import threading
import shutil
import os

HOST = "localhost"
PORT = 8081

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
agent = "server"

files = []

def debug_print(message):
    print(f"[debug] | [{message}]")

try:
    client.connect((HOST,PORT))
    print(f'Connected Successfully to {HOST}:{PORT}')
except:
    print(f'ERROR: Please review your host')

def split_message (chunk):
   array = chunk.split('|')
   return array

def receive_message():
    while True:
        # try:
            message = client.recv(1024).decode()
            debug_print(f"message: {message}")
            if message == 'agent':
                client.send(agent.encode())
            else:
                message = split_message(message)
                choice = int(message[0])
                file_name = message[1]
                level = int(message[2])
                file_size = int(message[3])

                print("Operação iniciada: "+ str(choice))
                debug_print(str(message))

                if(choice == 1):
                    client.send("Recebendo arquivo...".encode())
                    files.append(file_name)

                    path = os.path.dirname(__file__)
                    file_path = os.path.join(path, "data", file_name)
                    with open(file_path, "wb") as file:
                        count = 0 
                        while count <= (file_size / 1024):
                            debug_print('receiving file chunk')
                            file_chunk = client.recv(1024)
                            file.write(file_chunk)
                            count += 1

                    output =  file_name +' salvo com sucesso'
                    client.send(output.encode())

                    if level > 0:
                        for i in range(level):
                            dest_path  = file_path + f".replica-{i + 1}"
                            shutil.copy(file_path, dest_path)
                        
                        output =  str(level) +' Replicas criadas com sucesso'
                        client.send(output.encode())
                  
                elif (choice == 2):
                    client.send("Buscando arquivo...".encode())

                    if file_name not in files: 
                      client.send((file_name + ' não encontrado').encode())
                      continue

                    output =  file_name + " encontrado com sucesso"
                    client.send(output.encode())
                    
                    client.send("Restaurando...".encode())

                    with open(file_path, "rb") as file:
                        while True:
                            data = file.read(1024)
                            debug_print('sending file chunk')
                            if not data:
                                break
                            client.send(data)

                    client.send("Arquivo Restaurado!".encode())



                   
                      
                      
                
        # except:
        #     print('[ERRO]')
        #     quit()

receive_message()