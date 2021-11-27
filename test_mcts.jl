#=
test_mcts:
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-25
=#

include("ConnectFourEnvironment.jl")
include("MonteCarloTreeSearch.jl")

state = ConnectFourEnvironment.create_env()
root_node = MonteCarloTreeSearch.create_node(state, missing, 3, 1)