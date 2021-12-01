#=
test_mcts:
- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-11-25
=#

module MonteCarloTreeSearchTests

    using ConnectFour.ConnectFourEnvironment
    using ConnectFour.MonteCarloTreeSearch
    using ConnectFour.PlayerRandom


    println("Start MonteCarloTreeSearchTests")
    state = create_env()
    player = create_player("rollout-player")
    root_node = create_node(state, missing, missing, 0.0)

    result = best_child(root_node, player, 10)
    println("best move: ",  result.state.last_action)
    println("result: ", result)
end