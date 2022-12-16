from pygame import init, QUIT, KEYDOWN, K_BACKSPACE, K_SPACE, K_RETURN, mouse, draw
from pygame.event import get
from pygame.display import update, flip
from pygame.font import Font
from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_STREAM
from threading import Thread
from pickle import dumps, loads
from canvas import Canvas

class Client(object):
    def __init__(self) -> None:
        init()

        # Socket information
        self.port = 53444
        self.ip = gethostbyname(gethostname())
        self.addr = (self.ip, self.port)
        self.client = socket(AF_INET, SOCK_STREAM)
        self.is_drawer = []
        self.information = {
            "X": None, 
            "Y": None, 
            "drawer": None,
            "word": "",
            "connected": True,
            "player_id": None,
            "player_id_won": None,
            "color": (0, 0, 0)
        }

        # Pygame information
        self.black_tuple = (0, 0, 0)
        self.white_tuple = (255, 255, 255)
        self.red_tuple = (255, 0, 0)
        self.green_tuple = (0, 255, 0)
        self.blue_tuple = (0, 0, 255)
        self.msgss = []
        self.width = int
        self.height = int
        self.board = None
        self.text = Font(None, 25)
        self.first_message = None
        self.red = None
        self.blue = None
        self.green = None
        self.black = None
        self.clear_button = None
        self.player_id = None

    def get_word(self, filename):
        """
        Reads in words from the words.json file and picks one at random. """

        f = open(filename)
        data = json.load(f)
        words = data["possible words"]
        word = random.choice(words)
        return word
        
    def connect(self) -> None:
        """
        Connects to a given server address and initiates threading the information between them.
        """
        try:
            self.client.connect(self.addr)
            Thread(target=self.recvmsgs).start()
        except Exception as e:
            print("Error connecting to server. Please run the server program first.")
            print(e)

    def recvmsgs(self) -> None:
        """
        Pickle loads incoming information and changes self.information accordingly.
        If a guesser, will update canvas as the drawer's x and y coordinates are sent in.
        """
        try:
            self.first_message = loads(self.client.recv(4096))
            if self.first_message["drawer"] == True:
                self.is_drawer.append(0)
            self.player_id = self.first_message["player_id"]
            while self.information["connected"] != False:
                # loads information from other clients
                self.information = loads(self.client.recv(4096))
                print(str(self.information["X"]) + " " + str(self.information["Y"]))

                if self.information["player_id_won"]:
                    player_who_has_won = self.information["player_id_won"]
                    losing_message = self.text.render(f"PLAYER {player_who_has_won} HAS WON. YOU ARE PLAYER {self.player_id}.", True, (0, 255, 0))
                    self.board.blit(losing_message, (0, 0))

                if not self.is_drawer:
                    self.information["color"] = self.get_color((self.information["X"], self.information["Y"]))
                    #clear canvas button
                    if self.clear_button.collidepoint((self.information["X"], self.information["Y"])):
                        draw.rect(self.board, self.white_tuple, (0,0,500,440))
                    draw.rect(self.board, self.information["color"], (self.information["X"], self.information["Y"], 10, 10))
                else:
                    drawer_text = self.text.render("YOU ARE A DRAWER", True, self.black_tuple)
                    string_text = "draw the word " + str(self.information["word"])
                    word_text = self.text.render(string_text, True, self.black_tuple)
                    self.board.blit(drawer_text, (200, 460))
                    self.board.blit(word_text, (200, 480))
        except Exception as e:
            print("Error in recvmsgs")
            print(e)

    def initialize_canvas(self):
        """
        creates the canvas, screen, and buttons
        """
        try:
            can = Canvas()
            can.canvas()
            can.buttons()
            self.height = can.height
            self.width = can.width
            self.board = can.get_screen()
            self.white_background = can.white_background
            self.red = can.red
            self.blue = can.blue
            self.green = can.green
            self.black = can.black
            self.clear_button = can.clear_button
        except Exception as e:
            print("Error in initialize_canvas")
            print(e)

    def get_color(self, coordinates: tuple) -> tuple:
        """
        If the color buttons are clicked, returns the colors corresponding tuple.
        e.g. (0, 0, 0) is black.
        """
        try:
            if self.red.collidepoint(coordinates):
                return self.red_tuple
            elif self.blue.collidepoint(coordinates):
                return self.blue_tuple
            elif self.green.collidepoint(coordinates):
                return self.green_tuple
            elif self.black.collidepoint(coordinates):
                return self.black_tuple
            else:
                # return what it already is.
                return self.information["color"]
        except Exception as e:
            print("Error in get_color")
            print(e)


    def sub(self) -> None:
        """
        Subscribing to the information being sent in.
        Key strokes, clicks, mouse movements, etc.
        """
        subscribed = True
        entered_message = ""
        while subscribed:
            for event in get():
                if event.type == QUIT:
                    self.information["connected"] = False
                    subscribed = False
                    quit()
                elif event.type == KEYDOWN and not self.is_drawer:
                    if event.key == K_BACKSPACE:
                        entered_message = ""
                        draw.rect(self.board, self.white_tuple, (200, 475, 200, 100))
                    elif event.key == K_SPACE:
                        pass
                    elif event.key == K_RETURN:
                        if not self.is_drawer:
                            if entered_message == self.information["word"]:
                                self.information["player_id_won"] = self.player_id
                                self.client.send(dumps(self.information))
                            entered_message = ""
                            draw.rect(self.board, self.white_tuple, (200, 475, 200, 100))
                    else:
                        if len(entered_message) < 10:
                            entered_message += event.unicode
                    rendered_entered_message = self.text.render(entered_message, True, self.black_tuple)
                    self.board.blit(rendered_entered_message, (200, 475))
                    flip()
                    
            
            if mouse.get_pressed()[0]:
                # If drawer is drawing, check color and send x, y coordinates to other clients.
                if self.is_drawer:
                    coordinates = mouse.get_pos()
                    if self.clear_button.collidepoint(coordinates):
                        draw.rect(self.board, self.white_tuple, (0,0,500,440))
                        self.client.send(dumps(self.information))
                    self.information["color"] = self.get_color(coordinates)
                    self.information["X"], self.information["Y"] = coordinates

                    if (self.information["Y"] <= 430):
                        draw.rect(self.board, self.information["color"], (self.information["X"], self.information["Y"], 10, 10))
                        self.client.send(dumps(self.information))

            update()