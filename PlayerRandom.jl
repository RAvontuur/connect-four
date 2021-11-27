#=
PlayerRandom
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-26
=#

module PlayerRandom

    import ConnectFourEnvironment
    import MonteCarloTreeSearch

    export Player
    export create_player, play

    mutable struct Player
        name
    end

    function create_player(name)
        return Player(name)
    end

#     function action_values(env :: connectfour.Environment):
#         result = [-1.0] * 7
#         for a in env.get_legal_actions()
#             result[a] = 0.0
#         end
#
#         return result

    function play(self::Player, env::connectfour.Environment, untried_actions = missing)
        @assert env.terminated == false

        if untried_actions == missing
            free_columns = connectfour.get_legal_actions(env)
            random.shuffle(free_columns)
        else
            free_columns = untried_actions
        end

        action = random.choice(free_columns)

        return move(env, action), action

    end
end