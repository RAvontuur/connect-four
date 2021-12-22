"""
# module PlayerMonteCarloRef

- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-12-04

# Examples

```jldoctest
julia>
```
"""
module PlayerMonteCarloRef

    using ConnectFour.ConnectFourEnvironment
    using ConnectFour.MonteCarloTreeSearchRef
    using ConnectFour.PlayerRandom

    using Random

    export Player
    export create_player, play

    OptionalActions = Union{Array{Int8},Missing}

    mutable struct Player
        name
        number_of_simulations
        play_func
    end

    function create_player(name, number_of_simulations)
        return Player(name, number_of_simulations, play)
    end

    function play(self::Player, env::Environment, untried_actions::OptionalActions = missing)
        @assert env.terminated == false

        root_node = create_node(env, missing, missing, 0.0)
        rollout_player = PlayerRandom.create_player("rollout-player")
        result = tree_search(root_node, rollout_player, self.number_of_simulations)
        action = result.state.last_action
        return move(env, action), action
    end
end