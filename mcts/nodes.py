import numpy as np
import random
from collections import defaultdict

class MonteCarloTreeSearchNode():

    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.children = []
        self.tried_actions = []
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self.untried_actions = self.state.get_legal_actions()
        random.shuffle(self.untried_actions)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def choices_weights(self, c_param=1.4):
        return [
            (c.q / (c.n)) + c_param * np.sqrt((2 * np.log(self.n) / (c.n)))
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

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    @property
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self.untried_actions.pop(0)
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(next_state, parent=self)
        self.children.append(child_node)
        self.tried_actions.append(action)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        player = self.state.next_to_move
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result(player)

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(-result)
