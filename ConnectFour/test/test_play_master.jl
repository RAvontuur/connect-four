"""
# module test_play_master

- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-12-04

# Examples

```jldoctest
julia>
```
"""
module test_play_master

    using ConnectFour.ConnectFourEnvironment
    using ConnectFour.PrintUtil
    using ConnectFour.PlayerRandom
    using ConnectFour.PlayerMonteCarlo

    function play_game()
        player1 = PlayerRandom.create_player("player-1")
        player2 = PlayerMonteCarlo.create_player("player-2")

        env = create_env()
        println("start playing")
        move_count = 0
        cur_player = 1
        while env.terminated == false
            @assert env.player == cur_player
            @assert env.reward == 0
            @assert env.move_count == move_count
            if cur_player == 1
                env, action = player1.play_func(player1, env, missing)
            else
                env, action = player2.play_func(player2, env, missing)
            end
            move_count = move_count + 1
            cur_player = -cur_player
            println(display_board(env))
        end
        @assert env.terminated == true
        @assert env.illegal_action == false
        @assert env.move_count == move_count
        @assert env.player == cur_player
    end

    play_game()

end