from mcts.nodes import *
from mcts.search import MonteCarloTreeSearch

class Player_MonteCarlo:

    def __init__(self,  player):
        self.player = player

    def play(self, env):
        assert(env.next_to_move == self.player)
        assert(env.terminated == False)
        root = TwoPlayersGameMonteCarloTreeSearchNode(state = env, parent = None)
        mcts = MonteCarloTreeSearch(root)

        sims = 100000
            # sims = int(input("Enter number of simulations"))
        best_node = mcts.best_action(sims)

        # print("root")
        # print(mcts.root.n)
        # print(mcts.root.state.next_to_move)
        print(mcts.root._results)
        print(mcts.root.choices_weights(c_param=0.))
        print(mcts.root.choices_q())
        print(mcts.root.choices_n())
        #
        # print("best node")
        # print(best_node.n)
        # print(best_node.state.next_to_move)
        # print(best_node._results)
        # print(best_node.choices_weights(c_param=0.))
        # print(best_node.choices_q())
        # print(best_node.choices_n())


        return best_node.state






