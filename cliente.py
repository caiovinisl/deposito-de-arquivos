import socket
import threading
import os
import uuid

HOST = "127.0.0.1"
PORT = 8080

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    agent = "client"
    client.connect((HOST,PORT))
    print(f'Connected Successfully to {HOST}:{PORT}')
except:
    print(f'ERROR: Please review your host: {HOST}:{PORT}')

def receiveMessage():
    while True:
        try:
            message = client.recv(2048).decode('ascii')
            if message == 'agent':
                client.send(agent.encode('ascii'))
            else:
                print(message)
        except:
            print('[ERRO]')

def send_message(op,file_name,client_id,level):
   chunk = op+"|"+file_name+"|"+str(client_id)+"|"+str(level)
   client.send(chunk.encode('ascii'))


client_id = str(uuid.uuid4())

while True:
    print("Menu:")
    print("1. Depositar arquivo")
    print("2. Recuperar arquivo")
    print("3. Sair")
    choice = int(input())

    match choice:
        case 1:
            file_name = input("nome do arquivo:")
            level = int(input("tolerância:"))
            
            receiver_thread = threading.Thread(target=receiveMessage,args=()) 
            sender_thread = threading.Thread(target=send_message,args=("0",file_name,client_id,level))

            receiver_thread.start()
            sender_thread.start()
        case 2:
            file_name = input("nome do arquivo:")
            
            receiver_thread = threading.Thread(target=receiveMessage,args=()) 
            sender_thread = threading.Thread(target=send_message,args=("1",file_name,client_id, 0))

            receiver_thread.start()
            sender_thread.start()
        case 3:
            break
        case _:
            print(f'Operação não encontrada')