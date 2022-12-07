# This module defines the Guesser class.  The Guesser has 60 seconds 
# to guess what the Drawer is drawing.  If correct, the Guesser wins,
# if not, the Guesser keeps guessing until time is up.  

from player import Player
class Guesser(Player):
    def __init__(self, num:int, word:str):
        super.__init__(num, word)

    def makeGuess(self):
        # read in data from stream
        # return guess
        pass

    def checkGuess(self, guess:str):
        if guess == self.word:
            return True
        else:
            return False
