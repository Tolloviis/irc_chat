import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 5000

def receive_messages(sock):
    """
    Funktio viestien lähettämiseen
    """
    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                break
            decoded_msg = msg.decode()

            # clearataan jotenki tuo outputti että näyttää siistimmältä
            sys.stdout.write("\r\033[K")
            sys.stdout.flush()

            # printataan tuleva message, tarkistetaan onko boldia
            if ": " in decoded_msg:
                name, message = decoded_msg.split(": ", 1)
                if message.startswith("b."):
                    print(f"{bold_start}{name}: {message[2:]}{bold_end}")
                else:
                    print(f"{name}: {message}")
            else:
                print(decoded_msg)

            # printataan tuo näkymä käyttäjälle
            sys.stdout.write(f"{username}> ")
            sys.stdout.flush()
        except:
            break

def send_message():
    """
    Funktio viestien lähettämiseen
    """
    while True:
        msg = input(f"{username}> ")
        if msg.lower() == 'exit':
            break
        client.sendall(msg.encode())


def get_username():
    """
    Funktio käyttäjänimen syöttämiseen
    """
    while True:
        username_input = input("Enter your username: ").strip()
        if username_input:
            return username_input
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

# vastaanotetaan serveriltä chatroom lista
chatrooms_list_str = client.recv(1024).decode()
room_name = select_or_create_room(chatrooms_list_str)
client.sendall(room_name.encode())

threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

# lähetetään viestejä
send_message()

client.close()
