#=
test_mcts:
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-25
=#

import ConnectFour.ConnectFourEnvironment
import ConnectFour.MonteCarloTreeSearch

state = ConnectFourEnvironment.create_env()
root_node = MonteCarloTreeSearch.create_node(state, missing, 3, 1)