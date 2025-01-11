import json
import os

from src.game.grid.grid import Grid


class Game:
    def __init__(self):
        self.player_ids = []
        self.grid = None

        self.state = None
        self.action = None

        self.init_game()

        self.played_party = [0 for _ in range(len(self.player_ids))]
        self.win_game = [0 for _ in range(len(self.player_ids))]
        self.loose_game = [0 for _ in range(len(self.player_ids))]


    def get_state(self):
        pass


    def retrieve_all_actions(self):
        pass

    # Init from specific configuration
    def init_game(self):
        config_path = os.path.join(os.getcwd(), "configuration/config.json")
        with open(config_path, 'r') as file:
            data = json.load(file)

        num_player = data['number_player']
        self.player_ids = [i+1 for i in range(num_player)]

        self.grid = Grid()
        self.grid.init_players(self.player_ids)


    def reset_game(self):
        self.grid = Grid()
        self.grid.init_players(self.player_ids)


    # Init all possible actions
    def init_actions(self):
        pass


    def play_action(self, id, action):
        cell = self.grid.get_player(id)
        return self.grid.play_action(cell, action)


    def get_score(self):
        pass


    def start_game(self, players, number_party):
        for i in range(len(players)):
            players[i].set_id(self.player_ids[i])

        for i in range(0, number_party):
            print(f"Game {i + 1} ____________________")
            current_player_index = 0
            while not self.end():
                print(f" Player {players[current_player_index].id}")
                current_player = players[current_player_index]
                current_player.perceive()

                good_action = False
                while not good_action:
                    action = current_player.decide()
                    good_action = self.play_action(players[current_player_index].id, action)
                print(self.grid)

                result = self.score_state()
                current_player.sleep(result)
                current_player_index = (current_player_index + 1) % len(players)

            self.reset_game()

        print(f"On {self.played_party} games, {self.win_game} were won and {self.loose_game} were lost")
        # TODO: result_games is the average result of the played parties and won parties
        result_games = 0
        print(f"score: {result_games}")


    def score_state(self):
        return 0


    def win(self):
        grid_size = (len(self.grid.tab) + 1) // 2
        player_position = []
        for id in self.player_ids:
            cell = self.grid.get_player(id)
            player_position.append(cell)

        for player in player_position:
            if player.id == 1 and player.x == grid_size * 2 - 2:  # Player 1 reaches the last row
                return player.id
            if player.id == 2 and player.x == 0:  # Player 2 reaches the first row
                return player.id
            if player.id == 3 and player.y == grid_size * 2 - 2:  # Player 3 reaches the last column
                return player.id
            if player.id == 4 and player.y == 0:  # Player 4 reaches the first column
                return player.id

        return 0


    def end(self):
        winner = self.win()
        if winner != 0:
            for id in self.player_ids:
                if id == winner:
                    self.win_game[id - 1] += 1
                else:
                    self.loose_game[id - 1] += 1
                self.played_party[id - 1] += 1
            return True
        return False

