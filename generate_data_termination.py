from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_random import Player_Random
from play_writer_json import PlayWriterJson
from env_logger import EnvLogger

env_logger = EnvLogger("rollouts.csv")

player_rollout = Player_Random()

print("test 1: start from the beginning")
ENV = ConnectFourEnvironment()
ENV.set_logger(env_logger)

PLAYER = Player_MonteCarlo(50000, rollout_player=player_rollout)
env2, action = PLAYER.play(ENV)

assert(env2.next_to_move == -1)
print("visits: " + str(PLAYER.visits()))
print("choices: " + str(PLAYER.choices()))
play_writer = PlayWriterJson()
PLAYER.log(play_writer)
assert(PLAYER.analyzed_result() is None)
# print(play_writer.get_json())

env_logger.close()
