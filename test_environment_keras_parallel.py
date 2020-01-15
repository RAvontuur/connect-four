from environment_keras import ConnectFourEnvironmentKeras
import numpy as np
import time

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

model = ConnectFourEnvironmentKeras().model

def rollout(num_plays, num_displays=10):
    print("rollout multiple plays, num_plays: " + str(num_plays))
    start = time.time()
    env = ConnectFourEnvironmentKeras(model=model, parallel_plays=num_plays)

    first_move = None
    next_move = np.zeros(num_plays, dtype=int)
    counter = 0
    while np.any(env.terminated == 0):
        if counter>50:
            print("maximum moves exceeded")
            break
        indices_tuple = np.nonzero(env.valid_actions)
        permutation = np.random.permutation(indices_tuple[0].shape[0])
        next_move[indices_tuple[0][permutation]] = indices_tuple[1][permutation]/2
        if first_move is None:
            first_move = next_move
        env.move(next_move)
        counter += 1
    end = time.time()
    for i in range(num_plays):
        if i>=num_displays:
            break
        print(env.display(play=i))
    reward0 = np.where(env.reward[:,0]>0.5, 1, 0)
    reward1 = np.where(env.reward[:,1]>0.5, 1, 0)

    histogram_first_move = np.histogram(first_move, np.arange(8))[0]
    histogram0_first_move = np.array(np.histogram(np.where(env.reward[:,0]>0.5, first_move, -1), np.arange(8))[0], dtype=float)
    histogram1_first_move = np.array(np.histogram(np.where(env.reward[:,1]>0.5, first_move, -1), np.arange(8))[0], dtype=float)
    probabilities = (histogram0_first_move - histogram1_first_move) / histogram_first_move

    print("reward: " + str(np.sum(reward0)) + " - " + str(np.sum(reward1)))
    print("histogram: " + str(histogram_first_move))
    print("probabilities: " + str(probabilities ))
    print("elapsed: "  + str(end - start))
    print("elapsed Keras: "  + str(env.timer1))
    print()

rollout(100, num_displays=10)
rollout(1000, num_displays=0)
rollout(5000, num_displays=0)
rollout(10000, num_displays=0)
rollout(100000, num_displays=0)

print("all tests OK")
