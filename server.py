import socket
import threading
import shutil
import os

HOST = "localhost"
PORT = 8081

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
agent = "server"

files = []

def debug_print(message):
    print(f"[{message}]")

try:
    client.connect((HOST, PORT))
    print(f"Conectado com sucesso a {HOST}:{PORT}")
except:
    print(f"ERRO: Falha ao conectar a {HOST}:{PORT}")


def split_message(chunk):
    array = chunk.split("|")
    return array


def receive_message():
    while True:

        message = client.recv(1024).decode()  # Recebe dados da camada de transporte
        debug_print(f"mensagem: {message}")

        if message == "agent":
            client.send(agent.encode())  # Envia dados para a camada de transporte
        else:
            message = split_message(message)
            choice = int(message[0])
            file_name = message[1]
            level = int(message[2])
            file_size = int(message[3])

            print("Operação iniciada: " + str(choice))
            debug_print(str(message))

            if choice == 1:
                client.send(
                    "Recebendo arquivo...".encode()
                )  # Envia dados para a camada de transporte
                files.append(file_name)

                path = os.path.dirname(__file__)
                file_path = os.path.join(path, "data", file_name)
                with open(file_path, "wb") as file:
                    count = 0
                    while count <= (file_size / 1024):
                        debug_print("Recebendo pedaço do arquivo")
                        file_chunk = client.recv(
                            1024
                        )  # Recebe dados da camada de transporte
                        file.write(file_chunk)
                        count += 1

                output = file_name + " salvo com sucesso"
                client.send(output.encode())  # Envia dados para a camada de transporte

                if level > 0:
                    for i in range(level):
                        dest_path = file_path + f".replica-{i + 1}"
                        shutil.copy(file_path, dest_path)

                    output = str(level) + " Replicas criadas com sucesso"
                    client.send(
                        output.encode()
                    )  # Envia dados para a camada de transporte

            elif choice == 2:
                client.send(
                    "Buscando arquivo...".encode()
                )  # Envia dados para a camada de transporte

                if file_name not in files:
                    client.send(
                        (file_name + " não encontrado").encode()
                    )  # Envia dados para a camada de transporte
                    continue

                output = file_name + " encontrado com sucesso\n"
                client.send(output.encode())  # Envia dados para a camada de transporte

                client.send(
                    "Restaurando...".encode()
                )  # Envia dados para a camada de transporte

                with open(file_path, "rb") as file:
                    while True:
                        data = file.read(1024)
                        debug_print("Enviando pedaço do arquivo")
                        if not data:
                            break
                        client.send(data)  # Envia dados para a camada de transporte

                client.send(
                    "Arquivo Restaurado!".encode()
                )  # Envia dados para a camada de transporte


receive_message()
