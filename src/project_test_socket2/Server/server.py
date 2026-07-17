import socket
import threading

HOST = "localhost"
PORT = 8000

clients = []


def handle_client(client_socket: socket.socket) -> None:
    while True:
        try:
            request = client_socket.recv(1024).decode("utf-8")

            if not request:
                print("Client disconnected.")
                break

            if request == "bye":
                break

            elif request == "ping":
                client_socket.sendall(b"pong")

            elif request == "name":
                client_socket.sendall(b"Python Server")

            elif request == "count":
                client_socket.sendall(str(len(clients)).encode())

            elif request.startswith("@everyone"):
                message = request.replace("@everyone", "", 1).strip()

                for client in clients:
                    if client != client_socket:
                        try:
                            client.sendall(message.encode("utf-8"))
                        except ConnectionResetError:
                            pass

            else:
                client_socket.sendall(b"Unknown command")

        except ConnectionResetError:
            print("Connection lost.")
            break

    if client_socket in clients:
        clients.remove(client_socket)

    client_socket.close()

    print("Client disconnected.")
    print(f"Connected clients: {len(clients)}")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server started on {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()

    clients.append(client_socket)

    print(f"Client connected: {addr}")
    print(f"Connected clients: {len(clients)}")

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket,)
    )

    thread.start()