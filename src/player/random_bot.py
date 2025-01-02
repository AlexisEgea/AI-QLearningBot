import random


class RandomBot:
    def __init__(self, game):
        self.game = game
        self.state = None
        self.action = {}


    def perceive(self, game):
        pass

    def decide(self):
        self.state = self.game.get_state()
        actions = self.game.get_actions()
        i = random.randint(0, len(actions)-1)
        action = actions[i]
        self.action = action

        return self.action

    # Save the party in the dataset
    def sleep(self, result):
        logFile= open( "data/game.csv", "a" )
        logFile.write( f"{self.state},{self.action},{result}\n" )
        logFile.close()