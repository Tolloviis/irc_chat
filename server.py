import socket
import threading

HOST = '127.0.0.1'
PORT = 5000
"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}
"""
servers = [("192.168.0.2", 5001), ("192.168.0.3", 5002)]    # Testausta varten pari serveriä

def create_server(host='127.0.0.1', port=5000):
    """
    Funktio jonka avulla voisi "luoda serverin" jonne toinen käyttäjä voisi liittyä
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Server running on {host}:{port}")

    clients = {}

    def handle_client(conn, addr):
        print(f"New connection from {addr}")

        # testikoodia #
        try:
            username = conn.recv(1024).decode().strip()
            clients[conn] = username
            print(f"{username} has connected from {addr}")
        except:
            clients[conn] = "Unknown"
        try:
            # tämä printtaa kaikille clienteille listan servereistä
            server_list_str = "\n".join(f"{idx+1}. {ip}:{port}" for idx, (ip, port) in enumerate(servers))
            message = f"Connected to server.\nAvailable servers:\n{server_list_str}\n"
            conn.sendall(message.encode())
        except:
            pass
        # testikoodia #

        while True:
            try:
                msg = conn.recv(1024)
                if not msg:
                    break
                full_msg = f"{clients[conn]} says: {msg.decode()}"
                print(full_msg)

                for client in clients:
                    if client != conn:
                        client.sendall(full_msg.encode())
            except:
                break

        del clients[conn]
        conn.close()
        print(f"Connection closed: {addr}")

    print(f"Server listening on {HOST}: {PORT}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
