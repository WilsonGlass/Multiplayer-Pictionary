import socket
import threading

PORT = 5050
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handleclient(conn, addr):
    while True:
        msg = conn.recv(64).decode("utf-8")
        if msg:
            print(msg)

def start():
    server.listen()
    print("SERVER LISTENING")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handleclient, args=(conn, addr)).start()
        print("CLIENT CONNECTED")
start()