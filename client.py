import pygame
import sys
import socket
import threading
import pickle

class Client:
    def __init__(self) -> None:
        pygame.init()

        # Socket information
        self.port = 5050
        self.ip = socket.gethostbyname(socket.gethostname())
        self.addr = (self.ip, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.information = {
            "X": None, 
            "Y": None, 
            "msg": None,
            "drawer": None
        }

        # Pygame information
        self.msgss = []
        self.word = "clown"
        self.width = 400
        self.height = 400
        self.pixels = 4
        self.screen = pygame.display.set_mode((self.width+200, self.height))
        pygame.display.set_caption("Pictionary")
        self.board = [[(255, 255, 255) for _ in range(self.width//self.pixels)] for _ in range(self.width//self.pixels)]
        self.istyping = False
        self.text = pygame.font.Font(None, 25)

    def connect(self) -> None:
        """
        Connects to a given server address and initiates threading the information between them.
        """
        self.client.connect(self.addr)
        threading.Thread(target=self.recvmsgs).start()

    def recvmsgs(self) -> None:
        """
        Pickle loads incoming information and changes self.information accordingly.
        If a guesser, will update canvas as the drawer's x and y coordinates are sent in.
        """
        info_recieved = pickle.loads(self.client.recv(64))
        print(info_recieved)
        self.information = info_recieved
        try:
            if self.information["drawer"] == False:
                self.board[self.information["X"]//self.information["Y"]][self.information["Y"]//self.pixels] = (0, 0, 0)
        except:
            self.msgss.append(info_recieved)

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
                        if self.information["drawer"] == False:
                            if entered_message not in self.msgss:
                                self.client.send(entered_message.encode("utf-8"))
                            if self.information["msg"] == self.word:
                                print("YOU WIN")
                            entered_message = ""
                    else:
                        entered_message += event.unicode
                    
            
            if pygame.mouse.get_pressed()[0]:
                if self.information["drawer"] == True:
                    print(self.information)
                    self.information["X"], self.information["Y"] = pygame.mouse.get_pos()
                    if self.information["X"] <= self.width:
                        self.client.send(pickle.dumps(self.information))
                        self.board[self.information["X"]//self.pixels][self.information["Y"]//self.pixels] = (0, 0, 0)

            for msgs in self.msgss:
                if msgs == self.word:
                    guess_text = self.text.render(msgs, True, (0, 255, 0))
                else:
                    guess_text = self.text.render(msgs, True, (255, 255, 255))
                self.screen.blit(guess_text, (self.width+20, 15*self.msgss.index(msgs)))


            pygame.draw.rect(self.screen, (255, 0, 255), ((self.width, self.height-20), (200, 20)))
            guess_being_entered = self.text.render(self.information["msg"], True, (255,255,255))
            self.screen.blit(guess_being_entered, (self.width+10, self.height-15))


            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    pygame.draw.rect(self.screen, self.board[i][j], ((i * self.pixels, j * self.pixels), (self.pixels, self.pixels)))

            pygame.display.update()