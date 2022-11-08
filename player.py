# This module defines the Player class.  A Player object is created for each 
# player of Pictionary.  The Player object has a unique ID and has access to 
# the word of the round.

class Player:
    def __init__(self, num:int, word:str):
        self.id = num
        self.word = word
  
