#=
test_player_random:
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-26
=#

import ConnectFour.ConnectFourEnvironment
import ConnectFour.PlayerRandom

player = PlayerRandom.create_player("player-1")
env = ConnectFourEnvironment.create_env()

# while env.terminated == false
#     PlayerRandom.play(player, env)
#     println(env)
# end
