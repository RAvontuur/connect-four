from environment import ConnectFourEnvironment
from mcts.nodes import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch

class MockPlayer:

    def __init__(self, actions):
        self.actions = actions

    def play(self, env, untried_actions=None):
        action = self.actions.pop(0)
        print("mock play " + str(action))
        return env.move(action), action


env = ConnectFourEnvironment()

rollout_player = MockPlayer([0, 6, 0, 6, 0, 6, 0,
                             6, 0, 6, 0, 6, 0])
root = MonteCarloTreeSearchNode(state=env, parent=None)
# manipulate the untried_actions
root.untried_actions = [0]

mcts = MonteCarloTreeSearch(root, rollout_player)

node = mcts.tree_policy()
assert(node.state.get_player() == -1)

result = mcts.rollout(node)
node.backpropagate(result)

node = mcts.tree_policy()
# manipulate the untried_actions
node.parent.untried_actions = [6]
assert(node.state.get_player() == 1)

result = mcts.rollout(node)
node.backpropagate(result)

print("root")
print(root.n)
print(root._results)
print(root.choices_weights(c_param=0.))
print(root.choices_q())
print(root.choices_n())
print(root.state)
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
print(node.state)

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

rollout_player = MockPlayer([3, 0, 0])
root = MonteCarloTreeSearchNode(state=env, parent=None)
# manipulate the untried_actions
root.untried_actions = [3]

assert(root.state.get_player() == -1)
print("root")
print(root.state)

mcts = MonteCarloTreeSearch(root, rollout_player)

node = mcts.tree_policy()
print("node first time")
assert(node.state.get_player() == 1)
print(node.state)

result = mcts.rollout(node)
node.backpropagate(result)

node = mcts.tree_policy()
assert(node.state.get_player() == -1)

# manipulate the untried_actions
node.parent.untried_actions = [6]
result = mcts.rollout(node)
node.backpropagate(result)

print("root")
print(root.n)
print(root._results)
print(root.choices_weights(c_param=0.))
print(root.choices_q())
print(root.choices_n())
print(root.state)
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
print(node.state)

assert(root._results[-1] == 2)
assert(node.parent._results[-1] == 0)
assert(node.parent._results[1] == 2)
assert(node._results[1] == 0)
assert(node._results[-1] == 1)