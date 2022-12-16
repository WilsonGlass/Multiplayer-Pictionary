# This module defines the Player class.  A Player object is created for each 
# player of Pictionary.  The Player object has a unique ID and has access to 
# the word of the round.
from json import load
from random import choice

class Player:
    def get_word(words_file: str="words.json", data_type: str="possible words") -> str:
        """
        Reads in words from the words.json file and picks one at random. 
        :param words_file: The name of the json file you would like to read
        :param data_type: Data type in json file you would like to read in.
        """

        f = open(words_file)
        data = load(f)
        words = data[data_type]
        word = choice(words)
        return word
  
