import socket
import threading
import os
import uuid

HOST = "localhost"
PORT = 8080

agent = "client"
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def receiveMessage():
    while True:
        # try:
            message = client.recv(1024).decode()
            if message == 'agent':
                client.send(agent.encode())
            if message == 'file':
                print('saving file... {message}')
            else:
                print("message: {message}")
        # except:
        #     print('[ERRO]')

def send_recover_message(op,file_name,client_id,level, file_size):
    chunk = op+"|"+file_name+"|"+str(level)+"|"+str(file_size)
    client.send(chunk.encode())

def send_deposit_message(op,file_name,client_id,level, file_size):
    chunk = op+"|"+file_name+"|"+str(level)+"|"+str(file_size)
    client.send(chunk.encode())
   
    path = os.path.dirname(__file__)
    file_path = os.path.join(path, file_name)
   
    with open(file_path, "rb") as file:
        while True:
            data = file.read(1024)
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

        match choice:
            case 1:
                file_name = input("nome do arquivo:")
                level = int(input("tolerância:"))

                path = os.path.dirname(__file__)
                file_path = os.path.join(path, file_name)
                file_size = os.path.getsize(file_path)
                
                receiver_thread = threading.Thread(target=receiveMessage,args=()) 
                sender_thread = threading.Thread(target=send_deposit_message,args=("0",file_name,client_id,level, file_size))

                receiver_thread.start()
                sender_thread.start()
            case 2:
                file_name = input("nome do arquivo:")
                
                receiver_thread = threading.Thread(target=receiveMessage,args=()) 
                sender_thread = threading.Thread(target=send_recover_message,args=("1",file_name,client_id, 0, 0))

                receiver_thread.start()
                sender_thread.start()
            case 3:
                break
            case _:
                print(f'Operação não encontrada')


def main():
    try:
        client.connect((HOST,PORT))
        print(f'Conectado ao host com sucesso ({HOST}:{PORT})')
        startup_menu()
    except:
        print("Erro ao conectar ao host")
        client.close()

if __name__ == "__main__":
    main()