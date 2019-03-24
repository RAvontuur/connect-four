import numpy as np
import random
from collections import defaultdict

class MonteCarloTreeSearchNode():

    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.children = []
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self.untried_actions = self.state.get_legal_actions()
        random.shuffle(self.untried_actions)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def choices_weights(self, c_param=1.4):
        # the children have the result from opponents viewpoint
        return [
            (-c.q / (c.n)) + c_param * np.sqrt((2 * np.log(self.n) / (c.n)))
            for c in self.children
        ]

    def choices_q(self):
        return [
            c.q
            for c in self.children
        ]

    def choices_n(self):
        return [
            c.n
            for c in self.children
        ]

    def best_child(self, c_param=1.4):
        # print(self.choices_q())
        # print(self.choices_n())
        weights = self.choices_weights(c_param)
        return self.children[np.argmax(weights)]

    @property
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def is_terminal_node(self):
        return self.state.is_game_over()


    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(-result)
