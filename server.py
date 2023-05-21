import socket
import os
import shutil

SERVER_ADDRESS = ('localhost', 8000)
DATA_DIR = 'data/'

def handle_deposit(client_socket):
    file_name = client_socket.recv(1024).decode()
    tolerance = int(client_socket.recv(1024).decode())
    file_path = os.path.join(DATA_DIR, file_name)

    # Ler o conteúdo do arquivo
    with open(file_path, 'wb') as file:
        data = client_socket.recv(1024)
        while data:
            file.write(data)
            data = client_socket.recv(1024)

    # Criar as réplicas do arquivo
    replicas = []
    for i in range(tolerance):
        replica_path = file_path + f'.replica{i}'
        shutil.copy(file_path, replica_path)
        replicas.append(replica_path)

    client_socket.sendall(b'Deposit completed.')
    client_socket.close()

def handle_recovery(client_socket):
    file_name = client_socket.recv(1024).decode()
    file_path = os.path.join(DATA_DIR, file_name)

    # Verificar se existem réplicas do arquivo
    replicas = [file_path] + [file_path + f'.replica{i}' for i in range(10)]
    valid_replicas = [replica for replica in replicas if os.path.exists(replica)]

    if valid_replicas:
        replica_path = valid_replicas[0]

        # Enviar o arquivo de volta para o cliente
        with open(replica_path, 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)

        client_socket.sendall(b'File recovered successfully.')
    else:
        client_socket.sendall(b'File not found.')

    client_socket.close()

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(1)
    print('Server is running...')

    while True:
        client_socket, client_address = server_socket.accept()
        request_type = client_socket.recv(1024).decode()

        if request_type == 'deposit':
            handle_deposit(client_socket)
        elif request_type == 'recovery':
            handle_recovery(client_socket)
        else:
            client_socket.sendall(b'Invalid request.')
            client_socket.close()

if __name__ == '__main__':
    main()