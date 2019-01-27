from mcts.nodes import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch

class Player_MonteCarlo:

    def __init__(self, number_of_simulations=1000):
        self.number_of_simulations = number_of_simulations

    def play(self, env):
        assert (env.terminated == False)
        root = MonteCarloTreeSearchNode(state=env, parent=None)
        mcts = MonteCarloTreeSearch(root)

        # sims = int(input("Enter number of simulations"))
        best_node = mcts.best_action(self.number_of_simulations)

        # print("root")
        # print(mcts.root.n)
        # print(mcts.root.state.next_to_move)
        # print(mcts.root._results)
        # print(mcts.root.tried_actions)
        # print(mcts.root.choices_weights(c_param=0.))
        # print(mcts.root.choices_q())
        # print(mcts.root.choices_n())
        #
        # print("best node")
        # print(best_node.n)
        # print(best_node.state.next_to_move)
        # print(best_node._results)
        # print(best_node.choices_weights(c_param=0.))
        # print(best_node.choices_q())
        # print(best_node.choices_n())

        # TODO return action
        return best_node.state, 0
