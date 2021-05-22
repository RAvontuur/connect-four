from mcts.nodes import MonteCarloTreeSearchNode


class MonteCarloTreeSearch:

    def __init__(self, node: MonteCarloTreeSearchNode, player=None):
        self.root = node
        self.player = player

    def best_child(self, number_of_rollouts):
        for i in range(0, number_of_rollouts):
            node = self.tree_policy()
            while node.analyzed_result is not None:
                # increase visits without rollouts
                node.backpropagate(node.analyzed_result)
                if self.root.analyzed_result is not None:
                    break
                node = self.tree_policy()

            if self.root.analyzed_result is not None:
                # print("Fully analyzed after: " + str(i))
                break

            result = self.rollout(node)
            node.backpropagate(result)

        # retrieve result: exploitation only
        return self.root.best_child(c_param = 0.)


    def tree_policy(self):
        current_node = self.root
        while current_node.analyzed_result is None:
            if not current_node.is_fully_expanded():
                # expand
                next_state = current_node.state.copy()
                next_state, action = self.player.play(next_state, current_node.untried_actions)
                current_node.untried_actions.remove(action)

                child_node = MonteCarloTreeSearchNode(next_state, parent=current_node)
                current_node.children.append(child_node)

                if child_node.analyzed_result is not None and child_node.analyzed_result <= 0:
                        # opponent loses or play ended in a draw
                        current_node.untried_actions = []
                        current_node.analyzed_result = -child_node.analyzed_result
                        current_node.children = [child_node]
                return child_node
            else:
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

    def rollout(self, node):
        next_to_move = node.state.get_player()
        current_rollout_state = node.state.copy()
        while not current_rollout_state.is_game_over():
            current_rollout_state, _ = self.player.play(current_rollout_state)
            # print(current_rollout_state)
        return current_rollout_state.game_result(next_to_move)
