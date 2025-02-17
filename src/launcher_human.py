from game.game import Game
from player.human import Human
from src.game.launcher import Launcher

if __name__ == '__main__':
    game = Game()
    print(game.grid)

    human = Human()
    robot = Human()

    launcher = Launcher(game, [human, robot])
    launcher.start_game(1)
