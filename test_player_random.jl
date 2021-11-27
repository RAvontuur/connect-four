#=
test_player_random:
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-26
=#

include("ConnectFourEnvironment.jl")
include("MonteCarloTreeSearch.jl")

player = player_random.create_player("player-1")
env = connectfour.create_env()

while env.terminated == false
    player_random.play(player, env)
    println(env)
end
