from src.player.player import Player


class Human(Player):
    def __init__(self):
        super().__init__(0)


    def perceive(self):
        pass


    def decide(self):
        action = input("your action:")
        return action


    def sleep(self, result):
        pass