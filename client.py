import pygame
import sys
import socket
import threading

PORT = 5050
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
msg = "hello server"
msg = msg.encode("utf-8")
client.send(msg)

pygame.init()
width=height=800
pixels = 8
screen = pygame.display.set_mode((width, height))
board=[[(255, 255, 255) for _ in range(width//pixels)] for _ in range(width//pixels)]

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
    
    if pygame.mouse.get_pressed()[0]:
        x,y = pygame.mouse.get_pos()
        board[x//pixels][y//pixels] = (0, 0, 0)


    for i in range(len(board)):
        for j in range(len(board[0])):
            pygame.draw.rect(screen, board[i][j], ((i * pixels, j * pixels), (pixels, pixels)))

    pygame.display.update()