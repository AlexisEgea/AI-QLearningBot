from src.utils.evaluation import Evaluation


class Launcher:
    def __init__(self, game, players):
        self.game = game
        self.players = players

    def start_game(self, number_party):
        for i in range(len(self.players)):
            self.players[i].set_id(self.game.player_ids[i])

        for i in range(0, number_party):
            print(f"Game {i + 1} ____________________")
            current_player_index = 0
            while not self.game.end():
                print(f" Player {self.players[current_player_index].id}")
                current_player = self.players[current_player_index]
                current_player.perceive()

                good_action = False
                while not good_action:
                    action = current_player.decide()
                    good_action = self.game.play_action(self.players[current_player_index], action)

                print(self.game.grid)

                self.game.score[current_player_index] = Evaluation.score(self.game)
                self.game.sum_score[current_player_index] += self.game.score[current_player_index]

                current_player.sleep(self.game.score[current_player_index])
                current_player_index = (current_player_index + 1) % len(self.players)

            self.game.reset_game()

        print(f"On {self.game.played_party} games, {self.game.win_game} were won and {self.game.loose_game} were lost")
        result_games = [s / n if n != 0 else 0 for s, n in zip(self.game.score, self.game.played_party)]
        print(f"score: {result_games}")