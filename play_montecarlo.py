from mcts.nodes import *
from mcts.search import MonteCarloTreeSearch
from environment import ConnectFourEnvironment

initial_board_state = ConnectFourEnvironment()
initial_board_state.set_play_level(-3)

root = TwoPlayersGameMonteCarloTreeSearchNode(state = initial_board_state, parent = None)
mcts = MonteCarloTreeSearch(root)

while True:
    sims = 1000
    # sims = int(input("Enter number of simulations"))
    best_node = mcts.best_action(sims)
    # print("root")
    # print(mcts.root.n)
    # print(mcts.root.state.next_to_move)
    # print(mcts.root._results)
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
    print("after best computed action (X)")
    if best_node.state.terminated:
        print(best_node.state)
        break

    best_node.state.invert_state()
    best_node.state.set_play_level(-1)
    best_node.state.make_O_action()
    print("after your latest move (O)")
    print(best_node.state)
    if best_node.state.terminated:
        break
    best_node.state.set_play_level(-3)

    root = TwoPlayersGameMonteCarloTreeSearchNode(state = best_node.state, parent = None)
    mcts = MonteCarloTreeSearch(root)


