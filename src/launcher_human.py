from game.game import Game
from player.human import Human

if __name__ == '__main__':
    game = Game()
    print(game.grid)

    human = Human()
    robot = Human()

    game.start_game([human, robot], 1)
