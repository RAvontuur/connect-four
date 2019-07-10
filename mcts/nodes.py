import numpy as np
import random
import math
from collections import defaultdict

class MonteCarloTreeSearchNode():

    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.children = []
        self._results = defaultdict(int)
        self.untried_actions = self.state.get_legal_actions()
        self._number_of_visits = 0.

        if self.state.is_game_over():
            self.analyzed_result = self.state.reward
        else:
            self.analyzed_result = None

        random.shuffle(self.untried_actions)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def all_analyzed(self):
        for c in self.children:
            if c.analyzed_result is None:
                return False

        return True

    def choices_q_norm(self):
        result = [0.0] * 7
        for c in self.children:
            result[c.state.last_action] = -c.q / c.n
        return result


    def choices_weights(self, c_param=1.4):
        # the children have the result from opponents viewpoint
        return [
            (-c.q / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
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
        weights = self.choices_weights(c_param)
        return self.children[np.argmax(weights)]

    def v(self):
        wins = self._results[1]
        loses = self._results[-1]
        draws = self._results[0]
        n = wins + loses + draws

        return  (wins - loses) / n

    @property
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(-result)
