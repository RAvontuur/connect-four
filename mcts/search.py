import copy
from mcts.nodes import MonteCarloTreeSearchNode

class MonteCarloTreeSearch:

    def __init__(self, node: MonteCarloTreeSearchNode, player=None):
        self.root = node
        self.player = player


    def best_action(self, simulations_number):
        for i in range(0, simulations_number):
            if i+1 % 10000 == 0:
                print("simulation " + str(i))
            node = self.tree_policy()
            reward = self.rollout(node)
            node.backpropagate(reward)
        # exploitation only
        return self.root.best_child(c_param = 0.)


    def tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                # expand
                next_state = copy.deepcopy(current_node.state)
                next_state, action = self.player.play(next_state, current_node.untried_actions)

                current_node.untried_actions.remove(action)
                child_node = MonteCarloTreeSearchNode(next_state, parent=current_node)
                current_node.children.append(child_node)
                return child_node
            else:
                current_node = current_node.best_child()
        return current_node

    def rollout(self, node):
        next_to_move = node.state.next_to_move
        current_rollout_state = copy.deepcopy(node.state)
        while not current_rollout_state.is_game_over():
            current_rollout_state, _ = self.player.play(current_rollout_state)
        return current_rollout_state.game_result(next_to_move)

