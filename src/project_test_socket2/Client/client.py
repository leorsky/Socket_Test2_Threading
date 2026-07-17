import socket
import threading

HOST = "localhost"
PORT = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def receive_messages() -> None:
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")

            if not message:
                print("\nServer closed.")
                break

            print(f"\nFriend: {message}")

        except (ConnectionResetError, OSError):
            break


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()


while True:
    try:
        message = input("You: ")

        client_socket.sendall(message.encode("utf-8"))

        if message == "bye":
            break

    except (ConnectionResetError, OSError):
        break


client_socket.close()