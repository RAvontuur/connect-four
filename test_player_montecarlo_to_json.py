from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_random import Player_Random
from play_writer_json import PlayWriterJson

player_rollout = Player_Random()

# test 1: start from the beginning
ENV = ConnectFourEnvironment()
PLAYER = Player_MonteCarlo(1000, rollout_player=player_rollout)
env2, action = PLAYER.play(ENV)

assert(env2.next_to_move == -1)

play_writer = PlayWriterJson()
PLAYER.log(play_writer)

# print(play_writer.get_json())

print("test 2:  player wins in next move")
ENV = ConnectFourEnvironment()
PLAYER = Player_MonteCarlo(1000, rollout_player=player_rollout)

assert(ENV.terminated == False)
moves = [
    0,0,
    1,1,
    2,2 ]

for move in moves:
    ENV.move(move)
# print(ENV.display())

env2, action = PLAYER.play(ENV)
assert(env2.next_to_move == -1)
assert(action == 3)
assert(PLAYER.analyzed_result() == 1)

play_writer = PlayWriterJson()
PLAYER.log(play_writer)
# print(play_writer.get_json())

print("test 3:  player wins in 2 moves")
ENV = ConnectFourEnvironment()
PLAYER = Player_MonteCarlo(10000, rollout_player=player_rollout)

assert(ENV.terminated == False)
moves = [
    1,1,
    2,2]


for move in moves:
    ENV.move(move)

env2, action = PLAYER.play(ENV)
assert(env2.next_to_move == -1)
print(env2.display())
assert(PLAYER.analyzed_result() == 1)
assert(action == 3)

play_writer = PlayWriterJson()
PLAYER.log(play_writer)
# print(play_writer.get_json())


print("test 4: start from a winning position")
ENV = ConnectFourEnvironment()
PLAYER = Player_MonteCarlo(10000, rollout_player=player_rollout)

# _______
# ____O__
# X___X__
# XO_XX_O
# OX_OOXX
# OX_XOOO
# X is playing now

assert(ENV.terminated == False)
moves = [
    3,3,
    3,4,
    1,0,
    1,4,
    4,5,
    4,6,
    5,0,
    6,6,
    0,4,
    0,1 ]

for move in moves:
    ENV.move(move)

print(ENV.display())

env2, action = PLAYER.play(ENV)
assert(env2.next_to_move == -1)
print(env2.display())
assert(PLAYER.analyzed_result() == 1)

#
# play_writer = PlayWriterJson()
# PLAYER.log(play_writer)

