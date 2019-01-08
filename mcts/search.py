from mcts.nodes import MonteCarloTreeSearchNode

class MonteCarloTreeSearch:

    def __init__(self, node: MonteCarloTreeSearchNode):
        print("init MonteCarloTreeSearch")
        self.root = node


    def best_action(self, simulations_number):
        for i in range(0, simulations_number):
            if i % 100 == 0:
                print("simulation " + str(i))
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        # exploitation only
        return self.root.best_child(c_param = 0.)


    def tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
