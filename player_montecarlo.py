from mcts.nodes import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch
from play_writer import PlayWriter
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

        play_writer = PlayWriter("mcts.txt", write=True)

        self.log_node(play_writer, mcts.root)
        play_writer.close()

    def log_node(self, play_writer, node):
        play_writer.write_play(node.state, node.v(), node.n)
        for c in node.children:
            self.log_node(play_writer, c)
