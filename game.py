from client import Client
from threading import Thread

def game() -> None:
    """
    Where pictionary is ran on a per client basis.
    """
    c = Client()
    c.connect()
    c.sub()

game()