import pygame
import sys
import socket
import threading
import json
import random

class Client:
    def __init__(self) -> None:
        pygame.init()

        # Socket information
        self.port = 5050
        self.ip = socket.gethostbyname(socket.gethostname())
        self.addr = (self.ip, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Pygame information
        self.isdrawer = []
        self.msgss = []
        self.word = self.get_word('words.json')
        self.x = int
        self.y = int
        self.width = 400
        self.height = 400
        self.pixels = 4
        self.screen = pygame.display.set_mode((self.width+200, self.height))
        pygame.display.set_caption("Pictionary")
        self.board = [[(255, 255, 255) for _ in range(self.width//self.pixels)] for _ in range(self.width//self.pixels)]
        self.istyping = False
        self.msg = ""
        self.text = pygame.font.Font(None, 25)

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
        self.client.connect(self.addr)
        threading.Thread(target=self.recvmsgs).start()

    def recvmsgs(self) -> None:
        self.msg = self.client.recv(64).decode("utf-8")
        if self.msg == "drawer":
            self.isdrawer.append(0)
        else:
            info_from_server = self.client.recv(300).decode("utf-8")
            try:
                self.x, self.y = info_from_server.split()
                self.x = int(self.x)
                self.y = int(self.y)
                if not self.isdrawer:
                    self.board[self.x//self.pixels][self.y//self.pixels] = (0, 0, 0)
            except:
                self.msgss.append(info_from_server)

    def sub(self) -> None:
        """
        Subscribing to the information being sent in.
        """
        subscribed = True
        entered_message = ""
        while subscribed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.width+20 <= event.pos[0] <= self.width+160 and self.height - 20 <= event.pos[1] <= self.height:
                        self.istyping=True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        entered_message = entered_message[:-1]
                    elif event.key == pygame.K_SPACE:
                        pass
                    elif event.key == pygame.K_RETURN:
                        if not self.isdrawer:
                            if entered_message not in self.msgss:
                                self.client.send(entered_message.encode("utf-8"))
                            if self.msg == self.word:
                                print("YOU WIN")
                            entered_message = ""
                    else:
                        entered_message += event.unicode

                if (entered_message != "drawer"):
                    self.msg = entered_message
                    
            
            if pygame.mouse.get_pressed()[0]:
                if self.isdrawer:
                    self.x, self.y = pygame.mouse.get_pos()
                    if self.x <= self.width:
                        self.client.send(f"{str(self.x)} {str(self.y)}".encode("utf-8"))
                        self.board[self.x//self.pixels][self.y//self.pixels] = (0, 0, 0)

            for msgs in self.msgss:
                if msgs == self.word:
                    guess_text = self.text.render(msgs, True, (0, 255, 0))
                else:
                    guess_text = self.text.render(msgs, True, (255, 255, 255))
                self.screen.blit(guess_text, (self.width+20, 15*self.msgss.index(msgs)))


            pygame.draw.rect(self.screen, (255, 0, 255), ((self.width, self.height-20), (200, 20)))
            guess_being_entered = self.text.render(self.msg, True, (255,255,255))
            self.screen.blit(guess_being_entered, (self.width+10, self.height-15))


            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    pygame.draw.rect(self.screen, self.board[i][j], ((i * self.pixels, j * self.pixels), (self.pixels, self.pixels)))

            pygame.display.update()
