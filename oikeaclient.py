import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

def receive_messages(sock):
    """
    Funktio viestien vastaanottamiseen
    """
    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                break
            decoded_msg = msg.decode()
            if decoded_msg.startswith("b."):
                print(f"\n{bold_start}{decoded_msg[2:]}{bold_end}\n> ", end="")
            else:
                print(f"\n{decoded_msg}\n> ", end="")
        except:
            break

def get_username():
    """
    Funktio käyttäjänimiä varten
    """
    while True:
        username = input("Enter your username: ").strip()
        if username:
            return username
        print("Username cannot be empty.")

def select_or_create_room(chatroom_list_str):
    """
    printataan lista chatroomeista, käyttäjä saa valita minne menee,
    tai luoda uuden. chatroom_list_str on vielä stringi, joka muutetaan
    listaksi splitlines() avulla.
    """
    print(chatroom_list_str)
    lines = chatroom_list_str.strip().splitlines()
    room_names = [line.split('. ', 1)[1] for line in lines if '. ' in line]

    while True:
        choice = input("Choose chatroom number or enter 0 to create new: ").strip()
        if choice == "0":
            return input("Enter new chatroom name: ").strip()
        elif choice.isdigit() and 1 <= int(choice) <= len(room_names):
            return room_names[int(choice)-1]
        else:
            print("Invalid selection. Try again.")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# BOLDIT
bold_start = "\033[1m"
bold_end = "\033[0m"

# kutsutaan se username funktio ja lähetetään serverille
username = get_username()
client.sendall(username.encode())

chatrooms_list_str = client.recv(1024).decode()
room_name = select_or_create_room(chatrooms_list_str)
client.sendall(room_name.encode())

threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

# lähetetään viestejä
while True:
    msg = input(f"{username}> ")
    if msg.lower() == 'exit':
        break
    client.sendall(msg.encode())

client.close()