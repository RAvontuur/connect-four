#=
MonteCarloTreeSearch:
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-25
=#

module MonteCarloTreeSearch

    using ConnectFour.ConnectFourEnvironment
    using ConnectFour.PlayerRandom

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
        untried_actions
        analyzed_result::Bool
    end

    OptionalNode = Union{Node, Missing}

    function create_node(state, parent::OptionalNode, action, action_value)
        return Node(
            parent,
            Node[],
            state,
            action,
            action_value,
            Dict(-1 => 0, 0 => 0, 1 => 0),
            0,
            [],
            false
        )
    end

    function best_child(root_node, player, number_of_rollouts)
        for i in 1:number_of_rollouts
            println("rollout: ", i)
            node = tree_policy(root_node)
#             while node.analyzed_result is not None:
#                 # increase visits without rollouts
#                 node.backpropagate(node.analyzed_result)
#                 if self.root.analyzed_result is not None:
#                     break
#                 node = self.tree_policy()
#
#             if self.root.analyzed_result is not None:
#                 print("Fully analyzed after: " + str(i))
#                 break
#
             result = rollout(player, node)
             backpropagate(node, result)
        end
#         # retrieve result: exploitation only
#         return self.root.best_child(c_param = 0.)
        return root_node
    end
#
    function tree_policy(root_node::Node)
          current_node = root_node
#         while current_node.analyzed_result is None:
#             if not current_node.is_fully_expanded():
#                 # expand
#                 next_state = current_node.state.copy()
#                 next_state, action = self.player.play(next_state, current_node.untried_actions)
#                 current_node.untried_actions.remove(action)
#
#                 child_node = MonteCarloTreeSearchNode(next_state, parent=current_node)
#                 current_node.children.append(child_node)
#
#                 if child_node.analyzed_result is not None and child_node.analyzed_result <= 0:
#                         # opponent loses or play ended in a draw
#                         current_node.untried_actions = []
#                         current_node.analyzed_result = -child_node.analyzed_result
#                         current_node.children = [child_node]
#                 return child_node
#             else:
#                 best_child = current_node.best_child()
#                 if best_child.analyzed_result == -1:
#                     # it is sure that the opponent will lose
#                     # no reason to look further
#                     current_node.analyzed_result = 1
#                 elif current_node.all_analyzed():
#                     # it will not be better then this
#                     current_node.analyzed_result = -best_child.analyzed_result
#                 else:
#                     # continue exploring the best move (= the best child)
#                     current_node = best_child
#
        return current_node
    end

    function rollout(player, node::Node)
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

end