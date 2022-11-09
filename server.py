import socket
import threading
import pickle

PORT = 5050
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
conns = []
guesser_information = {
            "X": None, 
            "Y": None, 
            "msg": None,
            "drawer": False
}
drawer_information = {
            "X": None, 
            "Y": None, 
            "msg": None,
            "drawer": True
}
pickled_player_information = pickle.dumps(guesser_information)
pickled_drawer_information = pickle.dumps(drawer_information)



def handleclient(conn, addr):
    """
    Distributes the information between each client.
    """
    conns.append(conn)
    if len(conns) >= 2:
        conns[0].send(pickled_drawer_information)
        for x in conns[1:]:
            x.send("".encode("utf-8"))
    while True:
        msg = conn.recv(64)
        if msg:
            for x in conns:
                x.send(msg)

def start():
    """
    Initializes the server to be connected to.
    """
    server.listen()
    print("SERVER LISTENING")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handleclient, args=(conn, addr)).start()
        print("CLIENT CONNECTED")
start()