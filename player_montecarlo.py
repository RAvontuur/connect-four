from mcts.nodes import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch
import numpy as np

def processState(env):
    state = env.state

    if env.next_to_move == 1:
        X = np.array([1.0, 0.0])
        O = np.array([0.0, 1.0])
    else:
        O = np.array([1.0, 0.0])
        X = np.array([0.0, 1.0])

    neural_state = np.zeros(shape=(7, 6, 2), dtype=np.float32)
    for row in range(6):
        for col in range(7):
            if state[col][row] == 1:
                neural_state[col][row] = X
            elif state[col][row] == -1:
                neural_state[col][row] = O

    return np.reshape([neural_state], [7 * 6 * 2]).tolist()



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

        # sims = int(input("Enter number of simulations"))
        best_node = mcts.best_child(self.number_of_simulations)

        self.log(mcts)
        self._mcts = mcts
        env  = best_node.state
        return env, env.last_action

    def get_boards_and_labels(self):
        [boards, labels, visits] = self.get_boards_and_labels_for_node(self._mcts.root, None, None, None)
        return boards, labels, visits

    def get_boards_and_labels_for_node(self, node, boards, labels, visits):

        board = processState(node.state)
        label = node.v()
        visit = node.n
        if boards is None:
            boards = [board]
            labels = [label]
            visits = [visit]
        else:
            boards.append(board)
            labels.append(label)
            visits.append(visit)

        for c in node.children:
            [boards, labels, visits] = self.get_boards_and_labels_for_node(c, boards, labels, visits)
        return boards, labels, visits

    def log(self, mcts):
        f = open("mcts.txt","w+")
        self.log_node(f, mcts.root, 0)
        f.close

    def log_node(self, f, node, level):
        # f.write(str(node.n) + "\n")
        # f.write(str(node._results) + "\n")
        # f.write(str(node.choices_weights(c_param=0.)) + "\n")
        # f.write(str(node.choices_q()) + "\n")
        # f.write(str(node.choices_n()) + "\n")
        # f.write(str(node.state))
        f.write(str(level))
        f.write(",")
        f.write(node.state.get_game_state_short())
        f.write(",")
        f.write(str(node.v()))
        f.write(",")
        f.write(str(node.n))
        f.write("\n")
        for c in node.children:
            self.log_node(f, c, level+1)
