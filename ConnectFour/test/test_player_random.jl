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
    move_count = 0
    cur_player = 1
    while env.terminated == false
        @assert env.player == cur_player
        @assert env.reward == 0
        @assert env.move_count == move_count
        global env, action = player.play_func(player, env, missing)
        global move_count = move_count + 1
        global cur_player = -cur_player
        println("action: ", action)
        println(env)
    end
    @assert env.terminated == true
    @assert env.illegal_action == false
    @assert env.move_count == move_count
    @assert env.player == cur_player
end