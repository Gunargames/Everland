
import socket
from threading import Thread

print("Server started. Waiting for connections...")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5050))
server.listen()

clients = []

def handle_client(conn):
    while True:
        try:
            data = conn.recv(1024).decode()
            broadcast(data, conn)
        except:
            clients.remove(conn)
            conn.close()
            break

def broadcast(data, origin):
    for client in clients:
        if client != origin:
            client.send(data.encode())

def receive():
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        Thread(target=handle_client, args=(conn,)).start()

receive()