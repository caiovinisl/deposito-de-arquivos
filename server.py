import socket
import threading

HOST = "127.0.0.1"
PORT = 8080

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
agent = "server"

files = []

try:
    client.connect((HOST,PORT))
    print(f'Connected Successfully to {HOST}:{PORT}')
except:
    print(f'ERROR: Please review your host')

def toArray (chunk):
   array = chunk.split('|')
   return array

def receive_message():
    while True:
        # try:
            message = client.recv(1024).decode()
            if message == 'agent':
                client.send(agent.encode())
            else:
                print("Mensagem recebida e armazenada: "+ message)
                msg = toArray(message)
                op = msg[0]
                file_name = msg[1]
                level = int(msg[2])
                file_size = int(msg[3])

                if(msg[0] == "0"):
                    print("OP 0")
                    files.append(msg[1])

                    count = 0

                    while count <= (file_size / 1024):
                        file_chunk = client.recv(1024).decode()
                        print(file_chunk)
                        count += 1

                    mensg = 'Arquivo "'+ msg[1] +'" armazenado com sucesso'
                    client.send(mensg.encode())
                  
                elif (msg[0] == "1"):
                   if msg[1] in files:
                      mensg = 'Arquivo "'+ files[files.index(msg[1])] +'" recuperado com sucesso' 
                      client.send(mensg.encode())
                   if msg[1] not in files: 
                      client.send('Arquivo não encontrado'.encode())
                      
                      
                
        # except:
        #     print('[ERRO]')

receive_message()