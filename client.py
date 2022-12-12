from pygame import init, key, QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_BACKSPACE, K_SPACE, K_RETURN, mouse, draw
from pygame.event import get
from pygame.display import set_caption, set_mode, update
from pygame.font import Font
from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_STREAM
from threading import Thread
from pickle import dumps, loads
from canvas import Canvas

class Client(object):
    def __init__(self) -> None:
        init()

        # Socket information
        self.port = 5050
        self.ip = gethostbyname(gethostname())
        self.addr = (self.ip, self.port)
        self.client = socket(AF_INET, SOCK_STREAM)
        self.is_drawer = []
        self.information = {
            "X": None, 
            "Y": None, 
            "msg": None,
            "drawer": None
        }

        # Pygame information
        self.msgss = []
        self.word = "clown"
        self.width = int
        self.height = int
        self.pixels = 4
        self.board = None
        self.istyping = False
        self.text = Font(None, 25)
        self.first_message = None
        self.red = None
        self.blue = None
        self.green = None
        self.black = None
        self.draw_color = (0, 0, 0)

    def connect(self) -> None:
        """
        Connects to a given server address and initiates threading the information between them.
        """
        try:
            self.client.connect(self.addr)
            Thread(target=self.recvmsgs).start()
        except Exception as e:
            print("Error connecting to server")
            print(e)

    def recvmsgs(self) -> None:
        """
        Pickle loads incoming information and changes self.information accordingly.
        If a guesser, will update canvas as the drawer's x and y coordinates are sent in.
        """
        try:
            self.first_message = loads(self.client.recv(4096))
            print("First message: ", self.first_message)
            if self.first_message["drawer"] == True:
                self.is_drawer.append(0)
            print("Is Drawer ", self.is_drawer)
            while True:
                # loads information from other clients
                self.information = loads(self.client.recv(4096))
                print(self.information)
                if not self.is_drawer:
                    self.draw_color = self.get_color((self.information["X"], self.information["Y"]))
                    if self.clear_button.collidepoint((self.information["X"], self.information["Y"])):
                        draw.rect(self.board, (255,255,255), (0,0,500,440))
                    draw.rect(self.board, self.draw_color, (self.information["X"], self.information["Y"], 10, 10))
                if self.information["msg"] != None:
                    self.msgss.append(self.information["msg"])
        except Exception as e:
            print("Error in recvmsgs")
            print(e)

    def initialize_canvas(self):
        """
        creates the canvas, screen, and buttons
        """
        can = Canvas()
        can.canvas()
        can.buttons()
        self.height = can.height
        self.width = can.width
        self.board = can.get_screen()
        self.red = can.red
        self.blue = can.blue
        self.green = can.green
        self.black = can.black
        self.clear_button = can.clear_button

    def get_color(self, coordinates: tuple) -> tuple:
        """
        If the color buttons are clicked, returns the colors corresponding tuple.
        e.g. (0, 0, 0) is black.
        """
        if self.red.collidepoint(coordinates):
            return (255,0,0)
        elif self.blue.collidepoint(coordinates):
            return (0,255,0)
        elif self.green.collidepoint(coordinates):
            return (0,0,255)
        elif self.black.collidepoint(coordinates):
            return (0,0,0)
        else:
            return self.draw_color


    def sub(self) -> None:
        """
        Subscribing to the information being sent in.
        """
        subscribed = True
        entered_message = ""
        while subscribed:
            for event in get():
                if event.type == QUIT:
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        entered_message = entered_message[:-1]
                    elif event.key == K_SPACE:
                        pass
                    elif event.key == K_RETURN:
                        if self.is_drawer:
                            if entered_message not in self.msgss:
                                #fix this at some point
                                self.client.send(entered_message.encode("utf-8"))
                            if self.information["msg"] == self.word:
                                print("YOU WIN")
                            entered_message = ""
                    else:
                        entered_message += event.unicode
                    
            
            if mouse.get_pressed()[0]:
                if self.is_drawer:
                    coordinates = mouse.get_pos()
                    if self.clear_button.collidepoint(coordinates):
                        draw.rect(self.board, (255,255,255), (0,0,500,440))
                    self.draw_color = self.get_color(coordinates)
                    self.information["X"], self.information["Y"] = coordinates

                    if self.information["X"] <= self.width:
                        self.client.send(dumps(self.information))
                        print(self.draw_color)
                        draw.rect(self.board, self.draw_color, (self.information["X"], self.information["Y"], 10, 10))

            #for msgs in self.msgss:
            #    if msgs == self.word:
            #        guess_text = self.text.render(msgs, True, (0, 255, 0))
            #    else:
            #        guess_text = self.text.render(msgs, True, (255, 255, 255))
            #    self.screen.blit(guess_text, (self.width+20, 15*self.msgss.index(msgs)))


            #draw.rect(self.screen, (255, 0, 255), ((self.width, self.height-20), (200, 20)))
            #guess_being_entered = self.text.render(self.information["msg"], True, (255,255,255))
            #self.screen.blit(guess_being_entered, (self.width+10, self.height-15))


            #for i in range(len(self.board)):
            #    for j in range(len(self.board[0])):
            #        draw.rect(self.screen, self.board[i][j], ((i * self.pixels, j * self.pixels), (self.pixels, self.pixels)))

            update()