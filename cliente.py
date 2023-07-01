import socket

PROXY_ADDRESS = ("localhost", 9000)


def deposit_file(file_name, tolerance):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(PROXY_ADDRESS)
        client_socket.sendall(b"deposit")

        client_socket.recv(1024)  # Aguardar confirmação do proxy

        client_socket.sendall(file_name.encode())
        client_socket.sendall(tolerance.encode())

        # Enviar o conteúdo do arquivo para o proxy
        with open(file_name, "rb") as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.sendall(data)

        response = client_socket.recv(1024).decode()
        if response == "File deposited successfully.":
            print("File deposited successfully.")
        else:
            print("File deposit failed.")


def recover_file(file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(PROXY_ADDRESS)
        client_socket.sendall(b"recovery")
        print("Sent recovery request to proxy")

        client_socket.sendall(file_name.encode())
        print(f"Sent file name: {file_name}")

        response = client_socket.recv(1024).decode()

        if response == "File recovered successfully.":
            # Receber o arquivo do proxy
            with open(file_name, "wb") as file:
                data = client_socket.recv(1024)
                while data:
                    file.write(data)
                    data = client_socket.recv(1024)

            print("File recovered successfully.")
        else:
            print("File not found.")


def main():
    while True:
        print("Menu:")
        print("1. Deposit file")
        print("2. Recover file")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            file_name = input("Enter the file name: ")
            tolerance = int(input("Enter the tolerance level: "))
            deposit_file(file_name, tolerance)
        elif choice == "2":
            file_name = input("Enter the file name to recover: ")
            recover_file(file_name)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
