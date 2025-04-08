import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break
            print(f"\n{msg.decode()}\n> ", end="")
        except:
            break

def get_username():
    while True:
        username = input("Enter your username: ").strip()
        if username:
            return username
        print("Username cannot be empty. Try again.")

username = get_username()
client.sendall(username.encode())

response = client.recv(1024).decode()  # Receive the confirmation or server list
print(response)  # Print the message from server

thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()


while True:
    msg = input(f"{username}> ")
    if msg.lower() == 'exit':
        break
    client.sendall(msg.encode())

client.close()
