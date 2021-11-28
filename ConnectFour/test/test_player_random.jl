#=
test_player_random:
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-26
=#

module PlayerRandomTests
    using ConnectFour.ConnectFourEnvironment
    using ConnectFour.PlayerRandom

    player = create_player("player-1")
    env = create_env()
    println("start playing")
    while env.terminated == false
        global env, action = PlayerRandom.play(player, env)
        println("action: ", action)
        println(env)
    end
end