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
                print("The client has disconnected.")
                break

            match request:
                case "ping":
                    client_socket.sendall(b"pong")
                case "name":
                    client_socket.sendall(b"Python Server")
                case "count":
                    client_socket.sendall(str(len(clients)).encode())
                case "bye":
                    client_socket.sendall(b"Goodbye!")
                    break
                case _:
                    client_socket.sendall(b"Unknown command")

        except ConnectionResetError:
            print("Client lost connection.")
            break

    client_socket.close()
    print('Client disconnected')


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server started on {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()

    clients.append(client_socket)

    print(f'Client connected: {addr}\n'
          f'Connected clients: {len(clients)}\n')



    thread = threading.Thread(target=handle_client,args=(client_socket,))
    thread.start()