from mcts.nodes import *
from mcts.search import MonteCarloTreeSearch
from environment import ConnectFourEnvironment

initial_board_state = ConnectFourEnvironment()
initial_board_state.set_play_level(-3)

root = TwoPlayersGameMonteCarloTreeSearchNode(state = initial_board_state, parent = None)
print("root initialized")
mcts = MonteCarloTreeSearch(root)
print("mcts initialized")

best_node = mcts.best_action(100000)
while True:
    print(best_node.state)
    print(best_node.n)
    if len(best_node.children) == 0:
        break
    best_node = best_node.best_child()


