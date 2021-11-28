#=
MonteCarloTreeSearch:
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-25
=#

module MonteCarloTreeSearch

    using ConnectFour.ConnectFourEnvironment

    export Node
    export create_node

    mutable struct Node
        parent::Union{Node, Missing}
        children::Array{Node}
        state::Environment
        action
        action_value
        results
        number_of_visits
        untried_actions
        analyzed_result
    end

    OptionalNode = Union{Node, Missing}

    function create_node(state, parent::OptionalNode, action, action_value)
        return Node(
            parent,
            Node[],
            state,
            action,
            action_value,
            [],
            0,
            [],
            missing
        )
    end

end