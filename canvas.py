import pygame


class Canvas(object):
    def __init__(self):
        pygame.init()
        self.drawColor = (0,0,0)
        self.screen = pygame.display.set_mode((500,500))
        pygame.display.set_caption("Pictionary")
        self.clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))
        pygame.display.flip()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
 
        self.loop = True
        self.press = False

        self.font = pygame.font.SysFont(None, 24)
        self.img = self.font.render('TIME: 60', True, (0,0,0))
        self.screen.blit(self.img, (420, 10))

        self.font = pygame.font.SysFont(None, 24)
        self.img2 = self.font.render('CLEAR', True, (0,0,0))
        self.screen.blit(self.img2, (420, 470))
        self.red = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(30,460,30,30))
        self.blue = pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(70,460,30,30))
        self.green = pygame.draw.rect(self.screen, (0,0,255), pygame.Rect(110,460,30,30))
        self.black = pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(150,460,30,30))

    def get_screen(self):
        return self.screen

    def canvas(self) -> None:
        while self.loop:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.loop = False

                self.font = pygame.font.SysFont(None, 24)
                self.img = self.font.render('TIME: 60', True, (0,0,0))
                self.screen.blit(self.img, (420, 10))

                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(0,450,500,50))
                pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(0,440,500,10))

                self.font = pygame.font.SysFont(None, 24)
                clear_button = pygame.draw.rect(self.screen, (100,100,100), (420,470,60,60))
                self.img2 = self.font.render('CLEAR', True, (0,0,0))
                self.screen.blit(self.img2, (420, 470))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if clear_button.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(self.screen, (255,255,255), (0,0,500,500))
                    elif self.red.collidepoint(pygame.mouse.get_pos()):
                        drawColor = (255,0,0)
                    elif self.blue.collidepoint(pygame.mouse.get_pos()):
                        drawColor = (0,255,0)
                    elif self.green.collidepoint(pygame.mouse.get_pos()):
                        drawColor = (0,0,255)
                    elif self.black.collidepoint(pygame.mouse.get_pos()):
                        drawColor = (0,0,0)
                
                px, py = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed() == (1,0,0):
                    pygame.draw.rect(self.screen, drawColor, (px,py,10,10))
        
                if event.type == pygame.MOUSEBUTTONUP:
                    self.press == False
                pygame.display.update()
                self.clock.tick(1000)
            except Exception as e:
                print(e)
                pygame.quit()
                
        pygame.quit()