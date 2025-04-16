import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

chatrooms = {}  # dictionary chatroomeille
clients = {}    # dictionary clienteille

def broadcast(room_name, message, exclude=None):
    """
    Funktio joka lähettää viestin kaikille
    käyttäjille tietyn chatroomin sisällä
    """
    for conn in chatrooms.get(room_name, []):
        if conn != exclude:
            try:
                conn.sendall(message.encode())
            except:
                continue

def handle_client(conn, addr):
    """
    Perus funktio joka on mielestäni tunneillakin tehty
    """
    try:
        # saadaan käyttäjänimi ja lisätään clients dictionaryyn
        username = conn.recv(1024).decode().strip()
        clients[conn] = (username, None)
    except:
        conn.close()
        return

    try:
        # lähetetään data avoimista chatroomeista
        chatroom_list = list(chatrooms.keys())
        chatroom_list_str = "\n".join(f"{idx+1}. {name}" for idx, name in enumerate(chatroom_list))
        conn.sendall(f"Available chatrooms:\n{chatroom_list_str}\n".encode())

        # vastaanotetaan huoneen nimi joka on uusi tai olemassa oleva
        room_name = conn.recv(1024).decode().strip()
        clients[conn] = (username, room_name)
        chatrooms.setdefault(room_name, []).append(conn)

        broadcast(room_name, f"{username} has joined the chatroom.", exclude=conn)
    
        # viestien lähettäminen
        while True:
            msg = conn.recv(1024)
            if not msg:
                break
            full_msg = f"{username}: {msg.decode()}"
            broadcast(room_name, full_msg, exclude=conn)
    except:
        pass
    finally:
        # poistetaan clientti sieltä client dictionarysta
        username, room = clients.pop(conn, ("Unknown", None))
        # poistetaan chatroom listalta
        if room in chatrooms:
            chatrooms[room].remove(conn)
            if not chatrooms[room]:
                del chatrooms[room]
        conn.close()
        broadcast(room, f"{username} has left the chatroom.")
        print(f"Connection closed from {addr}")


def create_server():
    """
    Luodaan tämä serveri
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    create_server()