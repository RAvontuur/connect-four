from environment import ConnectFourEnvironment


# test X wins (vertical)
env = ConnectFourEnvironment()
assert(env.terminated == False)
assert(env.next_to_move == 1)
env.move(0)
assert(env.next_to_move == -1)
env.move(6)
assert(env.next_to_move == 1)
env.move(0)
assert(env.next_to_move == -1)
env.move(6)
assert(env.next_to_move == 1)
env.move(0)
assert(env.next_to_move == -1)
env.move(6)
assert(env.next_to_move == 1)
env.move(0)

assert(env.next_to_move == -1)
assert(env.terminated == True)
assert(env.game_result(1) == 1)
assert(env.game_result(-1) == -1)

# test 0 wins (vertical)
env = ConnectFourEnvironment()
assert(env.terminated == False)
assert(env.next_to_move == 1)
env.move(0)
assert(env.next_to_move == -1)
env.move(6)
assert(env.next_to_move == 1)
env.move(0)
assert(env.next_to_move == -1)
env.move(6)
assert(env.next_to_move == 1)
env.move(0)
assert(env.next_to_move == -1)
env.move(6)
assert(env.next_to_move == 1)
env.move(1)
assert(env.next_to_move == -1)
env.move(6)
assert(env.next_to_move == 1)
assert(env.terminated == True)
assert(env.game_result(1) == -1)
assert(env.game_result(-1) == 1)

print("all tests OK")
