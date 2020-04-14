from mcts.nodes import MonteCarloTreeSearchNodeDef, MonteCarloTreeSearchNode


class MonteCarloTreeSearch:

    def __init__(self, node: MonteCarloTreeSearchNodeDef, player=None):
        self.root = node
        self.player = player

    def best_child(self, number_of_rollouts) -> MonteCarloTreeSearchNodeDef:
        for i in range(number_of_rollouts):
            leaf_node = self.find_leaf_node()
            if leaf_node.analyzed_result is not None:
                # increase visit without roll outs
                leaf_node.back_propagate(leaf_node.analyzed_result)
            else:
                if leaf_node.env is None:
                    best_child: MonteCarloTreeSearchNodeDef = leaf_node
                else:
                    self.expand_node(leaf_node)
                    best_child: MonteCarloTreeSearchNodeDef = leaf_node.best_child()
                self.ensure_state_presence(best_child)
                if best_child.analyzed_result is not None:
                    best_child.back_propagate(best_child.analyzed_result)
                else:
                    result = self.roll_out(best_child)
                    best_child.back_propagate(result)

            if self.root.analyzed_result is not None:
                print("Fully analyzed after: " + str(i))
                break

        # retrieve final result: exploitation only
        result = self.root.best_child(c_param = 0.)
        if result.env is None:
            print("final best child has only a prior")
            self.ensure_state_presence(result)
        return result

    def find_leaf_node(self) -> MonteCarloTreeSearchNodeDef:
        current_node = self.root
        while current_node.is_fully_expanded() and current_node.analyzed_result is None:
            best_child = current_node.best_child()
            if best_child.analyzed_result == -1:
                # it is sure that the opponent will lose
                # no reason to look further
                current_node.analyzed_result = 1
            elif current_node.all_analyzed():
                # it will not be better then this
                current_node.analyzed_result = -best_child.analyzed_result
            else:
                # continue exploring the best move (= the best child)
                current_node = best_child
        return current_node

    def expand_node(self, leaf_node: MonteCarloTreeSearchNodeDef):
        assert(not leaf_node.is_fully_expanded())
        prior_values = self.player.prior_values(leaf_node.env)
        for i, prior_value in enumerate(prior_values):
            action = leaf_node.env.get_legal_actions()[i]
            child_node = MonteCarloTreeSearchNode(parent=leaf_node, action=action, prior_value=-prior_value)
            leaf_node.children.append(child_node)

    def ensure_state_presence(self, node: MonteCarloTreeSearchNodeDef):
        if node.env is None:
            self.ensure_state_presence(node.parent)
            env = node.parent.env.copy()
            node.env = env.move(node.action)
            if node.env.is_game_over():
                node.analyzed_result = node.env.game_result(node.env.get_player())

    def roll_out(self, node: MonteCarloTreeSearchNodeDef):

        next_to_move = node.env.get_player()
        current_rollout_env = node.env.copy()
        while not current_rollout_env.is_game_over():
            current_rollout_env, _ = self.player.play(current_rollout_env)
            # print(current_rollout_state)
        return current_rollout_env.game_result(next_to_move)
