import socket

SERVER_ADDRESS = ('localhost', 8000)

def deposit_file(file_name, tolerance):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDRESS)
        client_socket.sendall(b'deposit')
        client_socket.sendall(file_name.encode())
        client_socket.sendall(str(tolerance).encode())

        # Enviar o conteúdo do arquivo para o servidor
        with open(file_name, 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)

        response = client_socket.recv(1024).decode()
        print(response)

def recover_file(file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDRESS)
        client_socket.sendall(b'recovery')
        client_socket.sendall(file_name.encode())

        response = client_socket.recv(1024).decode()

        if response == 'File recovered successfully.':
            # Receber o arquivo do servidor
            with open(file_name, 'wb') as file:
                data = client_socket.recv(1024)
                while data:
                    file.write(data)
                    data = client_socket.recv(1024)

            print('File recovered successfully.')
        else:
            print('File not found.')

def main():
    while True:
        print('Menu:')
        print('1. Deposit file')
        print('2. Recover file')
        print('3. Exit')
        choice = input('Select an option: ')

        if choice == '1':
            file_name = input('Enter the file name: ')
            tolerance = int(input('Enter the tolerance level: '))
            deposit_file(file_name, tolerance)
        elif choice == '2':
            file_name = input('Enter the file name to recover: ')
            recover_file(file_name)
        elif choice == '3':
            break
        else:
            print('Invalid choice.')

if __name__ == '__main__':
    main()
