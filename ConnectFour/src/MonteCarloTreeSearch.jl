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
    export create_node, tree_search

    mutable struct Node
        parent::Union{Node, Missing}
        children::Array{Node}
        state::Environment
        action::Union{Int8, Missing}
        result::Float64
        number_of_visits::Int32
        untried_actions::Array{Int8}
        analyzed_result::Union{Int8, Missing}
    end

    OptionalNode = Union{Node, Missing}

    function create_node(state::Environment, parent::OptionalNode, action)

        untried_actions = get_legal_actions(state)
        shuffle!(untried_actions)

        if state.terminated == true
            analyzed_result = state.reward
        else
            analyzed_result = missing
        end

        return Node(
            parent,
            Node[],
            state,
            action,
            0.0,
            0,
            untried_actions,
            analyzed_result
        )
    end

    function tree_search(root_node::Node, player::Player, number_of_rollouts::Int64)
        for i in 1:number_of_rollouts
            node = tree_policy(root_node)
            while ismissing(node.analyzed_result) == false
                # increase visits without rollouts
                backpropagate(node, convert(Float64, node.analyzed_result))
                if ismissing(root_node.analyzed_result) == false
                    break
                end
                node = tree_policy(root_node)
            end

            if ismissing(root_node.analyzed_result) == false
                println("Fully analyzed after: ", i)
                break
            end

            node = new_child_node(node, player)
            if node.number_of_visits == 0
                predict(node.parent)
                node = tree_policy(root_node)
            end

            result = rollout(player, node)
            backpropagate(node, convert(Float64, result))
        end
        # retrieve result: exploitation only
        return best_child(root_node, 0.0)
    end
#
    function tree_policy(root_node::Node)
        current_node = root_node
        while shouldContinueExploring(current_node)
            # continue exploring the best move (= the best child)
            # go deeper
            current_node = best_child(current_node)
        end
        return current_node
    end

    function shouldContinueExploring(current_node::Node)
        if any_child_losing(current_node)
            return false
        end
        if is_fully_expanded(current_node) == false
            return false
        end
        if all_childs_winning(current_node)
            return false
        end

        return true
    end

    function new_child_node(current_node::Node, player::Player)
        # expand
        child_node = missing
        while length(current_node.untried_actions) > 0
            next_state = create_copy(current_node.state)
            next_state, action = player.play_func(player, next_state, current_node.untried_actions)
            filter!(e->e!=action, current_node.untried_actions)

            child_node = create_node(next_state, current_node, action)
            push!(current_node.children, child_node)
            if ismissing(child_node.analyzed_result) == false && child_node.analyzed_result == -1
                # the player of the node knows what to play in order to win
                current_node.analyzed_result = 1
                current_node.children = [child_node]
                return child_node
            end
        end
        return child_node
    end

    function predict(parent_node::Node)
        for c in parent_node.children
            backpropagate(c, 0.0)
            # dummy model
            # if c.action
        end
    end

    function rollout(player::Player, node::Node)
        next_to_move = node.state.player
        if node.state.terminated == true
            return game_result(node.state, next_to_move)
        end

        current_rollout_state = create_copy(node.state)
        while current_rollout_state.terminated == false
            current_rollout_state, action = player.play_func(player, current_rollout_state)
        end
        return game_result(current_rollout_state, next_to_move)
    end

    function backpropagate(node::Node, result::Float64)
        node.number_of_visits += 1
        node.result += result
        if ismissing(node.parent) == false
            backpropagate(node.parent, -result)
        end
    end

    function is_fully_expanded(node::Node)
        return length(node.untried_actions) == 0
    end

    function all_childs_winning(node::Node)
        for c in node.children
            if ismissing(c.analyzed_result) || c.analyzed_result != 1
                # at least one of the childs has no analyzed result or any other result than winning
                return false
            end
        end
        # the player of the node loses always (if opponent knows how)
        node.analyzed_result = -1
        return true
    end

    function any_child_losing(node::Node)
        for c in node.children
            if ismissing(c.analyzed_result) == false && c.analyzed_result == -1
                # the player of the node knows what to play in order to win
                node.analyzed_result = 1
                return true
            end
        end
        return false
    end

    function best_child(node::Node, c_param::Float64 = 1.4)
        @assert length(node.children) > 0
        weights = choices_weights(node, c_param)
        return node.children[argmax(weights)]
    end

    function choices_weights(node::Node, c_param)
        # the children have the result from opponents viewpoint
        return [
            child_weight(c, node.number_of_visits, c_param)
            for c in node.children
        ]
    end

    function child_weight(child::Node, parent_visits::Int32, c_param)
        if child.number_of_visits == 0
            return -child.result +  c_param * sqrt(2 * log(parent_visits))
        end
        return -child.result / child.number_of_visits + c_param * sqrt(2 * log(parent_visits) / child.number_of_visits)
    end
end