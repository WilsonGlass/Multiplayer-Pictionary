import pygame


class Canvas:
    def __init__(self):
        """
        Trying to figure out how to make this canvas useful because pygame GUI seems to just run in a while loop...
        """
        self.width = 400
        self.height = 400
        self.pixels = 4

    def create_window(self):       
        window = pygame.display.set_mode((self.width+200, self.height))
        return window

    def create_screen(self):
        screen=[[(255, 255, 255) for _ in range(self.width//self.pixels)] for _ in range(self.width//self.pixels)]
        return screen

    def get_width_height(self):
        return self.width, self.height

    def get_pixel_ratio(self):
        return self.pixels