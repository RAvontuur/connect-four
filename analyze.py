import logging

from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_random import Player_Random

logging.getLogger().setLevel(logging.INFO)


number_of_simulations = 5000000
player_rollout = Player_Random()
player1 = Player_MonteCarlo(number_of_simulations, rollout_player=player_rollout)
env = ConnectFourEnvironment()
env, action = player1.play(env)
player1.log_to_file("mcts.txt")
