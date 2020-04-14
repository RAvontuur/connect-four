from collections import defaultdict

import numpy as np

from environment import ConnectFourEnvironment


class MonteCarloTreeSearchNodeDef:

    def __init__(self, env: ConnectFourEnvironment):
        self.env = env
        self.action = None

    def back_propagate(self, result):
        pass


class MonteCarloTreeSearchNode(MonteCarloTreeSearchNodeDef):

    def __init__(self, env: ConnectFourEnvironment = None, parent: MonteCarloTreeSearchNodeDef = None, action=None,
                 prior_value=0.0):
        super().__init__(env)
        if env is None:
            self.action = action
        else:
            self.action = env.get_last_action()
        self.prior_value = prior_value
        self.parent = parent
        self.children = []
        self._results = defaultdict(int)
        self._number_of_visits = 0.

        if self.env is not None and self.env.is_game_over():
            self.analyzed_result = self.env.reward
        else:
            self.analyzed_result = None

    def is_fully_expanded(self):
        return len(self.children) > 0

    def all_analyzed(self):
        for c in self.children:
            if c.analyzed_result is None:
                return False

        return True

    def choices_q_norm(self):
        # by default: reward of an illegal move
        result = [-1.0] * 7
        for c in self.children:
            result[c.action] = -c.q / c.n
        return result

    def weight(self, c_param):
        if self.n == 0:
            return self.prior_value
        return (self.q / self.n) - c_param * np.sqrt((2 * np.log(self.parent.n) / self.n))

    def choices_weights(self, c_param=1.4):
        # the children have the result from opponents viewpoint
        if self.n == 0:
            weights = [
                -c.prior_value
                for c in self.children
            ]
        else:
            weights = [
                -c.weight(c_param)
                for c in self.children
            ]
        return weights

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

    def best_child(self, c_param=1.4) -> MonteCarloTreeSearchNodeDef:
        weights = self.choices_weights(c_param)
        return self.children[np.asarray(weights).argmax()]

    def v(self):
        wins = self._results[1]
        loses = self._results[-1]
        draws = self._results[0]
        n = wins + loses + draws

        return (wins - loses) / n

    @property
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def back_propagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.back_propagate(-result)
