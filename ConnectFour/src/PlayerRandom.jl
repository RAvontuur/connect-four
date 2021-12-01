#=
PlayerRandom
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-26
=#

module PlayerRandom

    using ConnectFour.ConnectFourEnvironment

    using Random

    export Player
    export create_player, play

    OptionalActions = Union{Array{Int8},Missing}

    mutable struct Player
        name
    end

    function create_player(name)
        return Player(name)
    end

    function play(self::Player, env::Environment, untried_actions::OptionalActions = missing)
        @assert env.terminated == false

        if ismissing(untried_actions) == true
            free_columns = get_legal_actions(env)
        else
            free_columns = untried_actions
        end

        shuffle!(free_columns)
        println("actions: ", free_columns)
        action = free_columns[1]
        return move(env, action), action

    end
end