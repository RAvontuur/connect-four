from mcts.nodes import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch
from environment import ConnectFourEnvironment
from player import Player


class PlayerMonteCarlo(Player):

    def __init__(self, number_of_simulations=7, rollout_player=None):
        self.number_of_simulations = number_of_simulations
        self.rollout_player = rollout_player
        self._mcts: MonteCarloTreeSearch = None

    def action_values(self, env: ConnectFourEnvironment):
        assert (not env.terminated)
        root = MonteCarloTreeSearchNode(parent=None, action_value=0.0, state=env)
        mcts = MonteCarloTreeSearch([root], self.rollout_player)
        self._mcts = mcts

        return mcts.root_nodes[0].choices_q_norm()

    def play(self, env: ConnectFourEnvironment):
        self._mcts = None
        assert (not env.terminated)
        root = MonteCarloTreeSearchNode(state=env, parent=None)
        mcts = MonteCarloTreeSearch([root], self.rollout_player)

        best_node = mcts.best_child(self.number_of_simulations)[0]

        self._mcts = mcts
        env = best_node.state
        return env, env.get_last_action()

    def analyzed_result(self, index=0):
        if self._mcts is None:
            return None
        if self._mcts.root_nodes[index].analyzed_result is None:
            return None
        return self._mcts.root_nodes[index].analyzed_result * self._mcts.root_nodes[index].state.get_player()

    def visits(self, index=0):
        if self._mcts is None:
            return None
        return self._mcts.root_nodes[index].n

    def choices(self, index=0):
        if self._mcts is None:
            return None
        return self._mcts.root_nodes[index].choices_q_norm()
