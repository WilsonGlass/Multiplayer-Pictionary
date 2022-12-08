from client import Client

def game() -> None:
    """
    Where pictionary is ran on a per client basis.
    """
    c = Client()
    c.initialize_canvas()
    c.connect()
    c.sub()

if __name__ == "__main__":
    game()