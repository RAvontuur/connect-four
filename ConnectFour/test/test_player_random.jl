#=
test_player_random:
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-26
=#

module PlayerRandomTests
    using ConnectFour.ConnectFourEnvironment
    using ConnectFour.PlayerRandom

    local player::PlayerRandom.Player = create_player("player-1")
    local env::ConnectFourEnvironment.Environment = create_env()

    # while env.terminated == false
    #     PlayerRandom.play(player, env)
    #     println(env)
    # end
end