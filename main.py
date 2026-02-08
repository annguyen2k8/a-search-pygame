from game import Game

if __name__ == "__main__":
    game = Game()
    try:
        game.mainloop()
    except Exception as error:
        raise error
