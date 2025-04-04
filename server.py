import socket
import threading

HOST='127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
servers = [("192.168.0.2", 5001), ("192.168.0.3", 5002)]    # Testausta varten pari serveriä

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    clients.append(conn)

    # testikoodia #
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
            print(f"{addr} says: {msg.decode()}")
            for client in clients:
                if client != conn:
                    client.sendall(msg)
        except:
            break

    clients.remove(conn)
    conn.close()
    print(f"Connection closed: {addr}")

print(f"Server listening on {HOST}: {PORT}...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn,addr))
    thread.start()
