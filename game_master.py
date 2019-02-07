import time
from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_neural import Player_Neural
from player_one_ahead import Player_One_Ahead
from player_random import Player_Random

number_of_plays = 10
show_play = True

i = 1

result_1 = 0.
result_2 = 0.

#player1 = Player_Neural()
# player2 = Player_Neural()
# player1 = Player_MonteCarlo(10000)
# player1 = Player_Random()
player_rollout = Player_One_Ahead()
# player_rollout = player1
# player_rollout = Player_Random()
player2 = Player_MonteCarlo(1000, rollout_player=player_rollout)
player1 = Player_One_Ahead()

start_tot = 0
while i <= number_of_plays:
    start = time.time() * 1000
    print("play " + str(i) + " starts")
    env = ConnectFourEnvironment()
    env.reset_board()

    while True:
        assert(env.next_to_move == 1)
        env, action = player1.play(env)
        if env.is_game_over():
            print(env)
            break

        assert(env.next_to_move == -1)
        env, action = player2.play(env)
        if env.is_game_over():
            print(env)
            break

        if show_play:
            print(env)

    if env.game_result(1) > 0:
        result_1 += 1.
    elif env.game_result(1) < 0:
        result_2 += 1.
    else:
        result_1 += 0.5
        result_2 += 0.5

    print("results: " + str(result_1) + " - " + str(result_2))
    elapsed = time.time() * 1000 - start
    start_tot += elapsed
    print("took (ms): " + str(int(elapsed)))

    i += 1

print("took (ms): " + str(start_tot/(i-1)))