from environment import ConnectFourEnvironment
from mcts.nodes import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch
from player import Player


class MockPlayer(Player):

    def __init__(self,  priors, actions):
        self.priors = priors
        self.actions = actions

    def prior_values(self, env: ConnectFourEnvironment):
        values = [0]*7
        values[self.priors.pop(0)] = 1
        return values

    def play(self, env):
        action = self.actions.pop(0)
        print("mock play " + str(action))
        return env.move(action), action


env = ConnectFourEnvironment()

rollout_player = MockPlayer(priors=[0, 6], actions=[6, 0, 6, 0, 6, 0, 0, 6, 0, 6, 0])
root = MonteCarloTreeSearchNode(env=env, parent=None)

mcts = MonteCarloTreeSearch(root, rollout_player)

leaf_node = mcts.find_leaf_node()
assert(leaf_node.env.get_player() == 1)
assert(leaf_node.env is not None)
mcts.expand_node(leaf_node)
assert(len(leaf_node.children) == 7)
best_child = leaf_node.best_child()
assert(best_child.action == 0)
assert(best_child.env is None)
mcts.ensure_state_presence(best_child)
assert(best_child.env is not None)
assert(best_child.env.last_action == 0)

# X wins (defined by the mocked actions), O is current player
result = mcts.roll_out(best_child)
assert(result == -1)
best_child.back_propagate(result)

node = mcts.find_leaf_node()
assert(node.action == 0)
assert(node.env.get_player() == -1)

# do another roll out
mcts.best_child(number_of_rollouts=1)
node = mcts.find_leaf_node()
assert(node.env.get_player() == 1)
assert(node.action == 6)

print("root")
print(root.n)
print(root._results)
print(root.choices_weights(c_param=0.))
print(root.choices_q())
print(root.choices_n())
print(root.env)
print("node.parent")
print(node.parent.n)
print(node.parent._results)
print(node.parent.choices_weights(c_param=0.))
print(node.parent.choices_q())
print(node.parent.choices_n())
print(node.parent.env)
print("node")
print(node.n)
print(node._results)
print(node.choices_weights(c_param=0.))
print(node.choices_q())
print(node.choices_n())
print(node.env)

assert(root._results[1] == 2)
assert(node.parent._results[1] == 0)
assert(node.parent._results[-1] == 2)
assert(node._results[-1] == 0)

print("start end game test")

env = ConnectFourEnvironment()
env.move(0)
env.move(1)
env.move(0)
env.move(2)
env.move(0)
assert(env.get_player() == -1)

rollout_player = MockPlayer(priors=[3], actions=[0, 0])

root = MonteCarloTreeSearchNode(env=env, parent=None)

assert(root.env.get_player() == -1)
print("root")
print(root.env)

mcts = MonteCarloTreeSearch(root, rollout_player)

node = mcts.find_leaf_node()
print("node first time")
assert(node.env.get_player() == 1)
print(node.env)

result = mcts.roll_out(node)
node.back_propagate(result)

node = mcts.find_leaf_node()
assert(node.env.get_player() == -1)

# manipulate the untried_actions
node.parent.untried_actions = [6]
result = mcts.roll_out(node)
node.back_propagate(result)

print("root")
print(root.n)
print(root._results)
print(root.choices_weights(c_param=0.))
print(root.choices_q())
print(root.choices_n())
print(root.env)
print("node.parent")
print(node.parent.n)
print(node.parent._results)
print(node.parent.choices_weights(c_param=0.))
print(node.parent.choices_q())
print(node.parent.choices_n())
print(node.parent.state)
print("node")
print(node.n)
print(node._results)
print(node.choices_weights(c_param=0.))
print(node.choices_q())
print(node.choices_n())
print(node.env)

assert(root._results[-1] == 2)
assert(node.parent._results[-1] == 0)
assert(node.parent._results[1] == 2)
assert(node._results[1] == 0)
assert(node._results[-1] == 1)