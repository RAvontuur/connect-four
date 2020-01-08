from environment_keras import ConnectFourEnvironmentKeras
from player_montecarlo import Player_MonteCarlo
from player_random import Player_Random
from play_writer_json import PlayWriterJson
from env_logger import EnvLogger
import time

env_logger = EnvLogger("rollouts-keras.csv",
                       [EnvLogger.LOG_BOARD_BEFORE_ACTION,
                        EnvLogger.LOG_ACTION,
                        EnvLogger.LOG_BOARD_AFTER_ACTION,
                        EnvLogger.LOG_CONNECT_FOUR_LABELS,
                        EnvLogger.LOG_VALID_MOVES_AFTER])

player_rollout = Player_Random()

print("start")

ENV = ConnectFourEnvironmentKeras()
ENV.verbose = True
# ENV.set_logger(env_logger)


PLAYER = Player_MonteCarlo(20, rollout_player=player_rollout)
start = time.time()
env2, action = PLAYER.play(ENV)
end = time.time()

print("elapsed: "  + str(end - start))
assert(env2.get_player() == -1)
print("visits: " + str(PLAYER.visits()))
print("choices: " + str(PLAYER.choices()))
# play_writer = PlayWriterJson()
# PLAYER.log(play_writer)
assert(PLAYER.analyzed_result() is None)
# print(play_writer.get_json())

env_logger.close()
