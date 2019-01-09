from mcts.nodes import *
from mcts.search import MonteCarloTreeSearch
from environment import ConnectFourEnvironment

initial_board_state = ConnectFourEnvironment()
initial_board_state.set_play_level(-3)

root = TwoPlayersGameMonteCarloTreeSearchNode(state = initial_board_state, parent = None)
mcts = MonteCarloTreeSearch(root)

while True:
    best_node = mcts.best_action(1000)
    print(best_node.n)
    print(best_node._results)
    print("after best action")
    if best_node.state.terminated:
        break

    best_node.state.invert_state()
    best_node.state.set_play_level(-1)
    best_node.state.make_O_action()
    print("after my move")
    print(best_node.state)
    if best_node.state.terminated:
        break
    best_node.state.set_play_level(-3)

    root = TwoPlayersGameMonteCarloTreeSearchNode(state = best_node.state, parent = None)
    mcts = MonteCarloTreeSearch(root)


