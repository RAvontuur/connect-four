import time
from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_neural import Player_Neural
from player_dnn_regressor import Player_DNN_Regressor
from player_one_ahead import Player_One_Ahead
from player_random import Player_Random

number_of_plays = 20
show_play = False
show_final_play = False
show_intermediate_result = False

def run():
    result_1 = 0.
    result_2 = 0.

    i = 1
    start_tot = 0
    while i <= number_of_plays:
        start = time.time() * 1000
        if show_intermediate_result:
            print("play " + str(i) + " starts")
        env = ConnectFourEnvironment()

        while True:
            assert(env.next_to_move == 1)
            env, action = player1.play(env)
            if env.is_game_over():
                if show_final_play:
                    print(env)
                break

            assert(env.next_to_move == -1)
            env, action = player2.play(env)
            if env.is_game_over():
                if show_final_play:
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

        if show_intermediate_result:
            print("results: " + str(result_1) + " - " + str(result_2))
        elapsed = time.time() * 1000 - start
        start_tot += elapsed
        # print("took (ms): " + str(int(elapsed)))

        i += 1

    if not show_intermediate_result:
        print("results: " + str(result_1) + " - " + str(result_2))

    # print("took (ms): " + str(start_tot/(i-1)))


print("starting")
for j in [1,7,10,20,30]:
    print("j : " + str(j))
    # player1 = Player_Neural()
    # player2 = Player_Neural()
    # player1 = Player_Random()
    # player_rollout = Player_One_Ahead()
    # player_rollout = Player_Neural()
    player_rollout1 = Player_DNN_Regressor()
    player_rollout2 = Player_Random()
    # player1 = Player_MonteCarlo(7, rollout_player=player_rollout1)
    player1 = player_rollout1
    player2 = Player_MonteCarlo(j, rollout_player=player_rollout2)
    # player2 = Player_One_Ahead()
    # player2 = Player_Neural()
    run()


