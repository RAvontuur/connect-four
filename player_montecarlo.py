from mcts.nodes import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch

class Player_MonteCarlo:

    def __init__(self, number_of_simulations=7, rollout_player=None):
        self.number_of_simulations = number_of_simulations
        self.rollout_player = rollout_player
        self._mcts = None

    def play(self, env):
        self._mcts = None
        assert (env.terminated == False)
        root = MonteCarloTreeSearchNode(state=env, parent=None)
        mcts = MonteCarloTreeSearch(root, self.rollout_player)

        best_node = mcts.best_child(self.number_of_simulations)

        self._mcts = mcts
        env  = best_node.state
        return env, env.last_action

    def analyzed_result(self):
        if self._mcts is None:
            return None
        if self._mcts.root.analyzed_result is None:
            return None
        return self._mcts.root.analyzed_result * self._mcts.root.state.next_to_move

    def visits(self):
        if self._mcts is None:
            return None
        return self._mcts.root.n

    def choices(self):
        if self._mcts is None:
            return None
        return self._mcts.root.choices_q_norm()
