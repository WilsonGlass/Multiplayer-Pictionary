from client import Client

def game() -> None:
    """
    Where pictionary is ran on a per client basis.
    """
    c = Client()
    c.connect()
    c.sub()

game()