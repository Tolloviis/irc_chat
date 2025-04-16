import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

bold_start = "\033[1m"
bold_end = "\033[0m"

def receive_messages():
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break
            print(f"\n{msg.decode()}\n> ", end="")
            if msg.startswith("b."):
                print(f"\n{bold_start}{msg.decode()}{bold_end}\n> ", end="")
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

response = client.recv(1024).decode()  # Tavallaan oottaa vastausta serveriltä jotta nää ei mee jotenki tyhmästi päällekkäin
print(response)  # printtaa serverit ja jotain

thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()


while True:
    msg = input(f"{username}> ")
    if msg.lower() == 'exit':
        break
    client.sendall(msg.encode())

client.close()
