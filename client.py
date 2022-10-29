import pygame
import sys
import socket
import threading

PORT = 5050
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
isdrawer = []
msgss = []

def recvmsgs():
    msg = client.recv(64).decode("utf-8")
    if msg == "drawer":
        isdrawer.append(0)
    while True:
        a = client.recv(300).decode("utf-8")
        try:
            x, y = a.split()
            x = int(x)
            y = int(y)
            if not isdrawer:
                board[x//pixels][y//pixels] = (0, 0, 0)
        except:
            msgss.append(a)



pygame.init()
width=height=400
pixels = 4
screen = pygame.display.set_mode((width+200, height))
board=[[(255, 255, 255) for _ in range(width//pixels)] for _ in range(width//pixels)]
font = pygame.font.Font(None, 25)
istyping = False
msg = ""
threading.Thread(target=recvmsgs).start()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if width+20 <= event.pos[0] <= width+160 and height - 20 <= event.pos[1] <= height:
                istyping=True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                msg = msg[:-1]
            elif event.key == pygame.K_RETURN:
                client.send(msg.encode("utf-8"))
            else:
                msg += event.unicode
    
    if pygame.mouse.get_pressed()[0]:
        if isdrawer:
            x,y = pygame.mouse.get_pos()
            if x <= width:
                client.send(f"{str(x)} {str(y)}".encode("utf-8"))
                board[x//pixels][y//pixels] = (0, 0, 0)

    for msgs in msgss:
        e = font.render(msgs, True, (255, 255, 255))
        screen.blit(e, (width+20, 15*msgss.index(msgs)))


    pygame.draw.rect(screen, (255, 0, 255), ((width+20, height-20), (140, 20)))
    m = font.render(msg, True, (255,255,255))
    screen.blit(m, (width+25, height-10))


    for i in range(len(board)):
        for j in range(len(board[0])):
            pygame.draw.rect(screen, board[i][j], ((i * pixels, j * pixels), (pixels, pixels)))

    pygame.display.update()