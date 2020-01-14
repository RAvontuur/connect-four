from environment_keras import ConnectFourEnvironmentKeras
import numpy as np

print("[0] test X wins (vertical)")
print("[1] test 0 wins (vertical)")
env = ConnectFourEnvironmentKeras(parallel_plays=2)
assert(np.all(env.terminated == False))
assert(env.get_player() == 1)
env.move([0,0])
assert(env.get_player() == -1)
env.move([6,6])
print(env.display())
assert(env.get_player() == 1)
env.move([0,0])
assert(env.get_player() == -1)
env.move([6,6])
assert(env.get_player() == 1)
env.move([0,0])
assert(env.get_player() == -1)
env.move([6,6])
assert(np.all(env.terminated == 0))
assert(env.get_player() == 1)
env.move([0,1])
assert(env.get_player(play=0) == 1)
assert(env.get_player(play=1) == -1)
assert(np.any(env.terminated == 0))
assert(np.any(env.terminated == 1))
dummy_move = 0
env.move([dummy_move,6])
print(env.display(play=0))
print(env.display(play=1))

assert(np.all(env.terminated == 1))
assert(env.get_player(play=0) == 1)
assert(env.get_player(play=1) == -1)
assert(env.game_result(1, play=0) == 1)
assert(env.game_result(-1, play=0) == -1)
assert(env.game_result(1, play=1) == -1)
assert(env.game_result(-1, play=1) == 1)


print("rollout multiple plays")
numplays=100
env = ConnectFourEnvironmentKeras(parallel_plays=numplays)
while np.any(env.terminated == 0):
    env.move(np.random.randint(low=0, high=6, size=numplays))

for i in range(numplays):
    print(env.display(play=i))


print("all tests OK")
