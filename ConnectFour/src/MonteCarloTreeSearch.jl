#=
MonteCarloTreeSearch:
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-25
=#

module MonteCarloTreeSearch

    using ConnectFour.ConnectFourEnvironment
    using ConnectFour.PlayerRandom

    using Random

    export Node
    export create_node, best_child

    mutable struct Node
        parent::Union{Node, Missing}
        children::Array{Node}
        state::Environment
        action::Union{Int8, Missing}
        action_value::Float32
        results::Dict
        number_of_visits::Int32
        untried_actions::Array{Int8}
        analyzed_result::Union{Int8, Missing}
    end

    OptionalNode = Union{Node, Missing}

    function create_node(state::Environment, parent::OptionalNode, action, action_value)

        untried_actions = get_legal_actions(state)
        shuffle!(untried_actions)

        if ismissing(state) == false && state.terminated == true
            analyzed_result = state.reward
        else
            analyzed_result = missing
        end

        return Node(
            parent,
            Node[],
            state,
            action,
            action_value,
            Dict(-1 => 0, 0 => 0, 1 => 0),
            0,
            untried_actions,
            analyzed_result
        )
    end

    function best_child(root_node::Node, player::Player, number_of_rollouts::Int64)
        for i in 1:number_of_rollouts
            println("rollout: ", i)
            node = tree_policy(root_node, player)
            while ismissing(node.analyzed_result) == false
                # increase visits without rollouts
                node.backpropagate(node.analyzed_result)
                if isMissing(root_node.analyzed_result) == false
                    break
                end
                node = tree_policy(root_node, player)
            end

            if ismissing(root_node.analyzed_result) == false
                println("Fully analyzed after: ", i)
                break
            end

            result = rollout(player, node)
            backpropagate(node, result)
        end
        # retrieve result: exploitation only
        return best_child(root_node, 0.0)
    end
#
    function tree_policy(root_node::Node, player::Player)
        println("tree policy:", root_node)
        current_node = root_node
        while ismissing(current_node.analyzed_result) == true
            if is_fully_expanded(current_node) == false
                # expand
                next_state = create_copy(current_node.state)
                next_state, action = play(player, next_state, current_node.untried_actions)
                filter!(e->e!=action, current_node.untried_actions)

                child_node = create_node(next_state, current_node, action, 0.0)
                push!(current_node.children, child_node)
                println("current node:", current_node)

                if ismissing(child_node.analyzed_result) == false && child_node.analyzed_result <= 0
                        # opponent loses or play ended in a draw
                        current_node.untried_actions = []
                        current_node.analyzed_result = -child_node.analyzed_result
                        current_node.children = [child_node]
                end
                return child_node
            else
                println("fully expanded")
                best_child_node = best_child(current_node)
                if ismissing(best_child_node.analyzed_result) == false && best_child_node.analyzed_result == -1
                    # it is sure that the opponent will lose
                    # no reason to look further
                    current_node.analyzed_result = 1
                elseif all_analyzed(current_node)
                    # it will not be better then this
                    current_node.analyzed_result = -best_child_node.analyzed_result
                else
                    # continue exploring the best move (= the best child)
                    current_node = best_child_node
                end
            end
        end
        return current_node
    end

    function rollout(player::Player, node::Node)
        next_to_move = node.state.player
        current_rollout_state = create_copy(node.state)
        println(current_rollout_state)
        while current_rollout_state.terminated == false
            current_rollout_state, action = play(player, current_rollout_state)
            println(current_rollout_state)
        end
        return game_result(current_rollout_state, next_to_move)
    end

    function backpropagate(node::Node, result::Int8)
        node.number_of_visits += 1
        node.results[result] += 1
        if ismissing(node.parent) == false
            backpropagate(node.parent, -result)
        end
    end

    function is_fully_expanded(node::Node)
        return length(node.untried_actions) == 0
    end

    function all_analyzed(node::Node)
        for c in node.children
            if ismissing(c.analyzed_result)
                return false
            end
        end
        return true
    end

    function best_child(node::Node, c_param::Float64 = 1.4)
        @assert length(node.children) > 0
        weights = choices_weights(node, c_param)
        println("choices_weights: ", weights)
        return node.children[argmax(weights)]
    end

    function choices_weights(node::Node, c_param)
        # the children have the result from opponents viewpoint
        return [
            (-q(c) / c.number_of_visits) + c_param * sqrt((2 * log(node.number_of_visits) / c.number_of_visits))
            for c in node.children
        ]
    end

    function q(node::Node)
        wins = node.results[1]
        loses = node.results[-1]
        return wins - loses
    end

    #     function v(node::Node)
#         wins = node.results[1]
#         loses = node.results[-1]
#         draws = node.results[0]
#         n = wins + loses + draws
#         return  (wins - loses) / n
#     end

end