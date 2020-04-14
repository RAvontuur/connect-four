from mcts.nodes import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch
from environment import ConnectFourEnvironment
from player import Player


class PlayerMonteCarlo(Player):

    def __init__(self, number_of_simulations=7, rollout_player=None):
        self.number_of_simulations = number_of_simulations
        self.rollout_player = rollout_player
        self._mcts: MonteCarloTreeSearch = None

    def prior_values(self, env: ConnectFourEnvironment):
        assert (not env.terminated)
        root = MonteCarloTreeSearchNode(parent=None, action_value=0.0, env=env)
        mcts = MonteCarloTreeSearch(root, self.rollout_player)
        self._mcts = mcts

        return mcts.root.choices_q_norm()

    def play(self, env: ConnectFourEnvironment):
        self._mcts = None
        assert (not env.terminated)
        root = MonteCarloTreeSearchNode(env=env, parent=None)
        mcts = MonteCarloTreeSearch(root, self.rollout_player)

        best_node = mcts.best_child(self.number_of_simulations)

        self._mcts = mcts
        env = best_node.env
        return env, env.get_last_action()

    def analyzed_result(self):
        if self._mcts is None:
            return None
        if self._mcts.root.analyzed_result is None:
            return None
        return self._mcts.root.analyzed_result * self._mcts.root.env.get_player()

    def visits(self):
        if self._mcts is None:
            return None
        return self._mcts.root.n

    def choices(self):
        if self._mcts is None:
            return None
        return self._mcts.root.choices_q_norm()
