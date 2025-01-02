from game.game import Game
from player.qLearner_bot import QLearnerBot

if __name__ == '__main__':
    game = Game()
    qLearner_bot = QLearnerBot(game)
    game.start_game(qLearner_bot, 10000)


