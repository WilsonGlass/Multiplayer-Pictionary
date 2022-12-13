# This module defines the Player class.  A Player object is created for each 
# player of Pictionary.  The Player object has a unique ID and has access to 
# the word of the round.
from json import load
from random import choice

class Player:
    def get_word(words_file="words.json", data_type="possible words"):
        """
        Reads in words from the words.json file and picks one at random. 
        """

        f = open(words_file)
        data = load(f)
        words = data[data_type]
        word = choice(words)
        return word
  
