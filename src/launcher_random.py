from game.game import Game
from player.random_bot import RandomBot

if __name__ == '__main__':
    game = Game()
    random_bot = RandomBot(game)
    game.start_game(random_bot, 10000)





