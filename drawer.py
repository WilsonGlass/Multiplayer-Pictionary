# This module defines the Drawer class.  The Drawer has 60 seconds 
# to draw an image that one of the Guessers can guess.  If correct, 
# If no one guesses correctly, the Drawer loses and has to draw again.

from Player import Player
class Drawer(Player):
    def __init__(self, num:int, word:str):
        super.__init__(num, word)

    def draw(self):
        pass
        
