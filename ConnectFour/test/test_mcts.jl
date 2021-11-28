#=
test_mcts:
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-25
=#

module MonteCarloTreeSearchTests

    using ConnectFour.ConnectFourEnvironment
    using ConnectFour.MonteCarloTreeSearch

    state = create_env()
    root_node = create_node(state, missing, 3, 1)

end