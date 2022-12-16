import pygame


class Canvas(object):
    def __init__(self):
        pygame.init()
        self.drawColor = (0,0,0)
        self.screen = pygame.display.set_mode((500,500))
        pygame.display.set_caption("Pictionary")
        self.screen.fill((255, 255, 255))
        pygame.display.flip()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.font = pygame.font.SysFont(None, 24)

    def get_screen(self):
        return self.screen

    def buttons(self):
        self.white_background = pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(0,450,500,50))
        self.red = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(30,460,30,30))
        self.blue = pygame.draw.rect(self.screen, (0,0,255), pygame.Rect(110,460,30,30))
        self.green = pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(70,460,30,30))
        self.black = pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(150,460,30,30))
        self.clear_button = pygame.draw.rect(self.screen, (100,100,100), (420,470,60,60))
        
    def canvas(self) -> None:
        try:
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(0,450,500,50))
            pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(0,440,500,10))

            self.font = pygame.font.SysFont(None, 24)
            self.img2 = self.font.render('CLEAR', True, (0,0,0))
            self.screen.blit(self.img2, (420, 470))
            
            pygame.display.update()
        except Exception as e:
            print(e)
            pygame.quit()