from environment import ConnectFourEnvironment
from player_random import Player_Random
from player_one_ahead import Player_One_Ahead
from player_manual import Player_Manual

env = ConnectFourEnvironment()

player1 = Player_One_Ahead(1)
player2 = Player_Manual(-1)

while True:
    env = player1.play(env)
    if env.is_game_over():
        print(env)
        break

    env = player2.play(env)
    if env.is_game_over():
        print(env)
        break