import socket

HOST = "localhost"
PORT = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    request  = input('Enter your message:')

    try:
        client_socket.sendall(request.encode("utf-8"))

        response = client_socket.recv(1024).decode("utf-8")

        if not response:
            print("Connection closed.")
            break

        print(response)

        if response == "Goodbye!":
            print("Connection closed.")
            break

    except ConnectionResetError:
        print("Connection lost.")
        break

client_socket.close()