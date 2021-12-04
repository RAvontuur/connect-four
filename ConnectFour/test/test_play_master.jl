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

    mutable struct GameResult
        player1::Float64
        player2::Float64
        move_count::Int64
    end

    function play_game(result::GameResult, print_level)
#         player1 = PlayerRandom.create_player("player-1")
        player1 = PlayerMonteCarlo.create_player("player-1", 10)
        player2 = PlayerMonteCarlo.create_player("player-2", 100)

        env = create_env()
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
            if (env.terminated)

            end
            move_count = move_count + 1
            cur_player = -cur_player
            if print_level == 2; println(display_board(env)) end
        end
        if print_level == 1; println(display_board(env)) end

        @assert env.terminated == true
        @assert env.illegal_action == false
        @assert env.move_count == move_count
        @assert env.player == cur_player

        if env.reward == 0
            result.player1 += 0.5
            result.player2 += 0.5
        elseif env.reward * cur_player > 0
            result.player1 += 1
        else
            result.player2 += 1
        end
        result.move_count += env.move_count
    end

    number_of_games = 10
    print_level = 2

    result = GameResult(0.0, 0.0, 0)
    @timev for i = 1:number_of_games
        play_game(result, print_level)
        if print_level > 0; println("Results: $(result.player1) - $(result.player2)") end
    end
    if print_level == 0; println("Results: $(result.player1) - $(result.player2)") end
    println("total moves count: $(result.move_count)")
end