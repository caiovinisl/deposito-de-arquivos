import socket
import threading
import os
import uuid

HOST = "localhost"
PORT = 8081

agent = "client"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def debug_print(message):
    print(f"[debug] | [{message}]")


def receiveMessage():
    while True:
        if client.fileno() == -1:
            break
        try:
            message = client.recv(1024).decode()
            if message == "agent":
                client.send(agent.encode())
            elif message == "file":
                print(f"saving file... {message}")
            else:
                print(f"message: {message}")
        except:
            print("Exit")


def send_recover_message(file_name, client_id, level, file_size):
    chunk = f"2|{file_name}|{level}|{file_size}"
    client.send(chunk.encode())


def send_deposit_message(file_name, client_id, level, file_size):
    chunk = f"1|{file_name}|{level}|{file_size}"
    client.send(chunk.encode())

    path = os.path.dirname(__file__)
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as file:
        while True:
            data = file.read(1024)
            debug_print("sending file chunk")
            if not data:
                break
            client.send(data)


client_id = str(uuid.uuid4())
replica_registry = {}


def startup_menu():
    while True:
        print("Menu:")
        print("1. Depositar arquivo")
        print("2. Recuperar arquivo")
        print("3. Sair")
        choice = int(input())

        if choice == 1:
            file_name = input("Nome do arquivo: ")
            level = int(input("Número de cópias: "))

            path = os.path.dirname(__file__)
            file_path = os.path.join(path, file_name)
            file_size = os.path.getsize(file_path)

            receiver_thread = threading.Thread(target=receiveMessage, args=())
            sender_thread = threading.Thread(
                target=send_deposit_message,
                args=(file_name, client_id, level, file_size),
            )

            receiver_thread.start()
            sender_thread.start()
            receiver_thread.join(0.5)
            sender_thread.join(0.5)

            # Atualizar o registro de réplicas
            if file_name in replica_registry:
                current_replicas = len(replica_registry[file_name])
                if level > current_replicas:
                    add_replicas(file_name, level - current_replicas)
                elif level < current_replicas:
                    remove_replicas(file_name, current_replicas - level)
            else:
                if level > 0:
                    add_replicas(file_name, level)

        if choice == 2:
            file_name = input("Nome do arquivo: ")

            receiver_thread = threading.Thread(target=receiveMessage, args=())
            sender_thread = threading.Thread(
                target=send_recover_message, args=(file_name, client_id, 0, 0)
            )

            receiver_thread.start()
            sender_thread.start()
            receiver_thread.join(0.5)
            sender_thread.join(0.5)
        if choice == 3:
            client.close()
            break
        if choice not in (1, 2, 3):
            print(f"Operação não encontrada")


def add_replicas(file_name, num_replicas):
    replicas = []
    for i in range(num_replicas):
        replica_name = f"{file_name}.replica-{i + 1}"
        replicas.append(replica_name)
    replica_registry[file_name] = replicas
    print(f"{num_replicas} réplicas adicionadas para o arquivo {file_name}")


def remove_replicas(file_name, num_replicas):
    replicas = replica_registry[file_name]
    removed_replicas = replicas[-num_replicas:]
    replica_registry[file_name] = replicas[:-num_replicas]
    print(f"{num_replicas} réplicas removidas para o arquivo {file_name}")
    print(f"Réplicas removidas: {removed_replicas}")


def main():
    try:
        client.connect((HOST, PORT))
        print(f"Conectado ao host com sucesso!")
        debug_print(f"host connected: ({HOST}:{PORT})")
        startup_menu()
    except:
        client.close()


if __name__ == "__main__":
    main()
