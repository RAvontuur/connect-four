#=
runTests:
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-27
=#

using Test

include("test_environment.jl")
include("test_mcts.jl")
include("test_player_random.jl")