import socket
import threading

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

clients = []
ids = []

servers = []
serversNames = []

def globalMessage(message):
   
   txt = servers[0]
   txt.send(message)
   
def globalM(message):
   txt = clients[0]
   txt.send(message)

def handleMessages(client,agent):
    while True:
        try:
           
            if agent == "client":
               receiveMessageFromClient = client.recv(2048).decode('ascii')
               globalMessage(f'{receiveMessageFromClient}'.encode('ascii'))
            elif agent == "server":
               receiveMessageFromClient = client.recv(2048).decode('ascii')
               globalM(f'{receiveMessageFromClient}'.encode('ascii'))
        except:
            client.close()


def initialConnection():
    while True:
        try:
            client, address = server.accept()
            print(f"New Connetion: {str(address)}")
            
            client.send('agent'.encode('ascii'))
            agent = client.recv(2048).decode('ascii')
            
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
            pass

initialConnection()