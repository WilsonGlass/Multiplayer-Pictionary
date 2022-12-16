from socket import gethostbyname, gethostname, socket,AF_INET, SOCK_STREAM
from threading import Thread
from pickle import dumps, loads
from player import Player

PORT = 53444
IP = gethostbyname(gethostname())
ADDR = (IP, PORT)
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
conns = []
word = Player.get_word()
guesser_information = {
            "X": 0, 
            "Y": 0,
            "drawer": False,
            "word": word,
            "connected": True,
            "player_id": None, #to be assigned
            "player_id_won": None,
            "color": (0, 0, 0)
}
drawer_information = {
            "X": 0, 
            "Y": 0,
            "drawer": True,
            "word": word,
            "connected": True,
            "player_id": 0, #to be assigned
            "player_id_won": None,
            "color": (0, 0, 0)
}
pickled_drawer_information = dumps(drawer_information)



def handleclient(conn: socket, addr: str) -> None:
    """
    Distributes the information between each client.
    :param conn: connection socket being handled
    :param addr: address of the client
    """
    try:
        print(f"[NEW CONNECTION] {addr} connected.")
        conns.append(conn)
        conns[0].send(pickled_drawer_information)
        if len(conns) >= 2:
            connection_index = conns.index(conn)
            
            if connection_index != 0:
                guesser_information["player_id"] = connection_index
                pickled_guesser_information = dumps(guesser_information)
                conns[connection_index].send(pickled_guesser_information)

        connected = True
        while connected:
            msg = conn.recv(4096)
            if msg:
                for x in conns:
                    x.send(msg)
            unpickled_message = loads(msg)
            if unpickled_message["connected"] == False:
                del conns[connection_index]
                connected = False
                conn.close()
            
    except Exception as e:
        print(f"Error in handleclient with ip {addr}")
        print(f"Error message: {e}")

def start() -> None:
    """
    Initializes the server to be connected to.
    """
    try:
        server.listen()
        print("SERVER LISTENING")
        while True:
            conn, addr = server.accept()
            Thread(target=handleclient, args=(conn, addr)).start()
            print("CLIENT CONNECTED")
    except Exception as e:
        print("Error starting server.")
        print(f"Error message: {e}")

if __name__=="__main__":
    start()