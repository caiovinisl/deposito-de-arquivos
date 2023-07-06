import socket
import threading

HOST = "localhost"
PORT = 8081

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

clients = []
ids = []

servers = []
serversNames = []

def globalMessage(message):
   
   txt = servers[-1]
   txt.send(message)
   
def globalM(message):
   txt = clients[-1]
   txt.send(message)

def handleMessages(client,agent):
    while True:
        try:
           
            if agent == "client":
               receiveMessageFromClient = client.recv(1024).decode()
               print("receiveMessageFromClient")
               print(receiveMessageFromClient)
               globalMessage(f'{receiveMessageFromClient}'.encode())
            elif agent == "server":
               receiveMessageFromClient = client.recv(1024).decode()
               print("receiveMessageFromClient")
               print(receiveMessageFromClient)
               globalM(f'{receiveMessageFromClient}'.encode())
        except:
            client.close()


def initialConnection():
    while True:
        try:
            client, address = server.accept()
            print(f"New Connetion: {str(address)}")
            
            client.send('agent'.encode())
            agent = client.recv(1024).decode()
            
            if agent == "client":
               clients.append(client)
               ids.append(agent)
               user_thread = threading.Thread(target=handleMessages,args=(client,agent,))
               user_thread.start()
            else:
               servers.append(client)
               serversNames.append(agent)
               user_thread = threading.Thread(target=handleMessages,args=(client,agent,))
               user_thread.start()
        except:
            quit()
            pass

try:
   initialConnection()
except:
   print('error')
   quit()