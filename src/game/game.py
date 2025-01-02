import json
import os
import random


class Game:
    def __init__(self):
        self.state = None
        self.action = None
        self.horizon = None

        self.played_party = 0
        self.win_game = 0
        self.loose_game = 0

    def get_state(self):
        pass

    def get_horizon(self):
        pass

    def retrieve_all_actions(self):
        pass

    # Init from specific configuration
    def init_game(self):
        pass

    def reset_game(self):
        pass

    # Init all possible actions
    def init_actions(self):
        pass

    def play_action(self, action):
        pass

    def get_score(self):
        pass


    def start_game(self, player, number_party):
        for i in range(0, number_party):
            print(f"Game {i+1} ____________________")
            # TODO: Add the first action depending on the game or remove the 3 next lines
            action = None
            self.play_action(action)
            self.score_state()
            while not self.end():
                player.perceive(self)
                action = player.decide()
                self.play_action(action)
                result = self.score_state()
                player.sleep(result)
            self.reset_game()
        print(f"On {self.played_party} games, {self.win_game} were won and {self.loose_game} were lost")
        # TODO: result_games is the average result of the played parties and won parties
        result_games = 0
        print(f"score: {result_games}")

    def score_state(self):
        return 0

    def win(self):
        # Check if the win condition of the game is met.
        # TODO: Implement the logic to determine if the player has won.
        if True:  # Replace 'True' with the actual win condition
            print("Game Win !!!")
            self.win_game += 1
            return True
        return False

    def loose(self):
        # Check if the lose condition of the game is met.
        # TODO: Implement the logic to determine if the player has lost.
        if True:  # Replace 'True' with the actual lose condition
            print("Game Loose :(")
            self.loose_game += 1
            return True
        return False

    def end(self):
        if self.win() or self.loose():
            self.played_party +=1
            return True
        return False

