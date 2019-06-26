from environment import ConnectFourEnvironment


env = ConnectFourEnvironment()

# test 1
test = "01O4T-__OX___X__________________________________"
env.set_game_state_short(test)

assert(env.move_count == 1)
assert(env.next_to_move == -1)
assert(env.last_action == 4)
assert(env.terminated == True)
assert(env.illegal_action == False)
assert(env.reward == -1)
assert(env.state[2][0] == -1)
assert(env.state[3][0] == 1)
assert(env.state[0][1] == 1)

round_trip = env.get_game_state_short()
print(round_trip)
assert(round_trip == test)

# test 2
test = "31X TI__OX___X_________________________________O"
env.set_game_state_short(test)

assert(env.move_count == 31)
assert(env.next_to_move == 1)
assert(env.last_action == None)
assert(env.terminated == True)
assert(env.illegal_action == True)
assert(env.reward == 1)
assert(env.state[6][5] == -1)

round_trip = env.get_game_state_short()
print(round_trip)
assert(round_trip == test)

# test 2
test = "00X   __OX___X_________________________________O"
env.set_game_state_short(test)

assert(env.move_count == 0)
assert(env.next_to_move == 1)
assert(env.last_action == None)
assert(env.terminated == False)
assert(env.illegal_action == False)
assert(env.reward == 0)
assert(env.state[6][5] == -1)

round_trip = env.get_game_state_short()
print(round_trip)
assert(round_trip == test)