from game.game import Game
from player.human import Human

if __name__ == '__main__':
    game = Game()
    human = Human()
    game.start_game(human, 1)
