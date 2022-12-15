import pygame

drawColor = (0,0,0)

# initialize canvas 
pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Pictionary")
clock = pygame.time.Clock()
screen.fill((255, 255, 255))
pygame.display.flip()
width = screen.get_width()
height = screen.get_height()
 
loop = True
press = False

font = pygame.font.SysFont(None, 24)
img = font.render('TIME: 60', True, (0,0,0))
screen.blit(img, (420, 10))

font = pygame.font.SysFont(None, 24)
img2 = font.render('CLEAR', True, (0,0,0))
screen.blit(img2, (420, 470))

# allows drawing while game is running
while loop:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        font = pygame.font.SysFont(None, 24)
        img = font.render('TIME: 60', True, (0,0,0))
        screen.blit(img, (420, 10))
    
        # creates color changing buttons
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(0,450,500,50))
        red = pygame.draw.rect(screen, (255,0,0), pygame.Rect(30,460,30,30))
        blue = pygame.draw.rect(screen, (0,255,0), pygame.Rect(70,460,30,30))
        green = pygame.draw.rect(screen, (0,0,255), pygame.Rect(110,460,30,30))
        black = pygame.draw.rect(screen, (0,0,0), pygame.Rect(150,460,30,30))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,440,500,10))

        font = pygame.font.SysFont(None, 24)
        clear_button = pygame.draw.rect(screen, (100,100,100), (420,470,60,60))
        img2 = font.render('CLEAR', True, (0,0,0))
        screen.blit(img2, (420, 470))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if clear_button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen,(255,255,255),(0,0,500,500))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if red.collidepoint(pygame.mouse.get_pos()):
                drawColor = (255,0,0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if blue.collidepoint(pygame.mouse.get_pos()):
                drawColor = (0,255,0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if green.collidepoint(pygame.mouse.get_pos()):
                drawColor = (0,0,255)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if black.collidepoint(pygame.mouse.get_pos()):
                drawColor = (0,0,0)
        
        px, py = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1,0,0):
            pygame.draw.rect(screen, drawColor, (px,py,10,10))
 
        if event.type == pygame.MOUSEBUTTONUP:
            press == False
        pygame.display.update()
        clock.tick(1000)
    except Exception as e:
        print(e)
        pygame.quit()
        
pygame.quit()

