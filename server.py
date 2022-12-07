from socket import gethostbyname, gethostname, socket,AF_INET, SOCK_STREAM
from threading import Thread
from pickle import dumps

PORT = 5050
IP = gethostbyname(gethostname())
ADDR = (IP, PORT)
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
conns = []
guesser_information = {
            "X": 0, 
            "Y": 0, 
            "msg": None,
            "drawer": False
}
drawer_information = {
            "X": 0, 
            "Y": 0, 
            "msg": None,
            "drawer": True
}
pickled_guesser_information = dumps(guesser_information)
pickled_drawer_information = dumps(drawer_information)



def handleclient(conn: socket, addr: str) -> None:
    """
    Distributes the information between each client.
    """
    conns.append(conn)
    conns[0].send(pickled_drawer_information)
    if len(conns) >= 2:
        connection_index = conns.index(conn)
        print("connection index ", connection_index)
        
        if connection_index != 0:
            conns[connection_index].send(pickled_guesser_information)

    while True:
        msg = conn.recv(64)
        if msg:
            for x in conns:
                x.send(msg)

def start() -> None:
    """
    Initializes the server to be connected to.
    """
    server.listen()
    print("SERVER LISTENING")
    while True:
        conn, addr = server.accept()
        Thread(target=handleclient, args=(conn, addr)).start()
        print("CLIENT CONNECTED")

if __name__=="__main__":
    start()