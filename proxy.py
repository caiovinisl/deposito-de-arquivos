# proxy.py

import socket
import threading
import random

PROXY_ADDRESS = ("localhost", 9000)
SERVER_ADDRESSES = [("localhost", 8000)]


def handle_client(client_socket):
    print("Handling client request")

    request = client_socket.recv(1024).decode().split()
    print(request)
    print(f"Received request type: {request[0]}")

    if request[0] == "deposit":
        server_socket = get_random_server_socket()
        if server_socket:
            server_socket.sendall(b"deposit ")

            file_name = request[1] + ' '
            server_socket.sendall(file_name.encode())

            tolerance = request[2]
            server_socket.sendall(tolerance.encode())

            # Enviar o conteúdo do arquivo ao servidor
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                server_socket.sendall(data)

            response = server_socket.recv(1024).decode().strip()
            client_socket.sendall(response.encode())
        else:
            client_socket.sendall(b"No server available.")

    elif request[0] == "recovery":
        server_socket = get_random_server_socket()
        if server_socket:
            server_socket.sendall(b"recovery ")

            file_name = request[1]
            server_socket.sendall(file_name.encode())

            response = server_socket.recv(1024).decode().strip()
            client_socket.sendall(response.encode())

            if response == "File recovered successfully.":
                # Enviar o arquivo de volta para o cliente
                while True:
                    data = server_socket.recv(1024)
                    if not data:
                        break
                    client_socket.sendall(data)
        else:
            client_socket.sendall(b"No server available.")

    client_socket.close()


def get_random_server_socket():
    if not SERVER_ADDRESSES:
        return None

    server_address = random.choice(SERVER_ADDRESSES)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.connect(server_address)
        return server_socket
    except ConnectionRefusedError:
        print(f"Connection refused to server {server_address}")
        SERVER_ADDRESSES.remove(server_address)
        return get_random_server_socket()


def main():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(PROXY_ADDRESS)
    proxy_socket.listen(1)
    print("Proxy is running...")

    while True:
        client_socket, client_address = proxy_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    main()
