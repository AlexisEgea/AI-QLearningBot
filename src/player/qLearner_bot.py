from matplotlib import pyplot as plt
import random

class QLearnerBot:
    def __init__(self, game):
        super().__init__()
        # Progress
        self._results = []
        self._evals = []

        # Q-Learning attributes
        self._qvalues = {}
        self.init_qvalue()

        self._learning_rate = 0.1
        self._epsilon = 1.0
        self.discount_factor = 0.99

        # TODO: Initialize the player ID to uniquely identify the player and determine
        #       which actions are available for them to perform during the game.
        #       Maybe add this field in parameter
        self._playerId = None
        self._game = game
        self._state = self._game.get_state()
        # TODO: Initialize the first action to play
        self._action = None

    def init_qvalue(self):
        # Init state in the qValues
        if self._state not in self._qvalues.keys():
            self._qvalues[self._state] = {}
        if self._action not in self._qvalues[self._state].keys():
            self._qvalues[self._state][self._action] = 0.0


    def update_qvalues(self, previous_state, action, current_state, reward):
        # If the state (current state or previous state) doesn't exist, initialise it
        if current_state not in self._qvalues.keys():
            self._qvalues[current_state] = {}
        if self._action not in self._qvalues[current_state].keys():
            self._qvalues[current_state][action] = 0.0
        if previous_state not in self._qvalues.keys():
            self._qvalues[previous_state] = {}
        if self._action not in self._qvalues[previous_state].keys():
            self._qvalues[previous_state][self._action] = 0.0

        # updating qValues
        experience = reward + self.discount_factor * max(self._qvalues[current_state].values())
        self._qvalues[previous_state][action] = (
                    (1 - self._learning_rate) * self._qvalues[previous_state][action] + self._learning_rate * experience)

    def perceive(self):
        new_state = self._game.get_state()
        new_score = self._game.get_score()
        # Learn:
        self.update_qvalues(self._state, self._action, new_state, new_score)
        # Switch
        self._state = new_state

    def decide(self):
        # TODO: Retrieve all possible actions
        actions = self._game.retrieve_all_actions()

        random_result = random.uniform(0, 1)
        if random_result < self._epsilon:
            self._action = random.choice(actions)
        else:
            self._action = max(self._qvalues[self._state], key=self._qvalues[self._state].get)

        return self._action

    def sleep(self, result):
        self._results.append(result)
        if len(self._results) == 500:
            self._epsilon /= 10
            self._evals.append(sum(self._results) / 500.0)
            self._results = []
            self.draw_evaluations()

    # For evaluation purpose
    def draw_evaluations(self):
        plt.plot(
            [i * 500 for i in range(len(self._evals))],
            self._evals)
        plt.savefig("evaluation_plot.png")
        plt.clf()
