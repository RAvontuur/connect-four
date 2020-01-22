import time
from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_random import Player_Random
from player_keras import PlayerKeras

number_of_plays = 1
show_play = True
show_final_play = True
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
            assert(env.get_player() == 1)
            env, action = player1.play(env)
            if env.is_game_over():
                if show_final_play:
                    print(env)
                break

            assert(env.get_player() == -1)
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

        # print("OK: {} NOK: {}".format(player1.env_keras.counterOK, player1.env_keras.counterNOK))

    if not show_intermediate_result:
        print("results: " + str(result_1) + " - " + str(result_2))

    # print("took (ms): " + str(start_tot/(i-1)))


print("starting")
player_rollout1 = Player_Random()
player1 = PlayerKeras(10000)
player2 = Player_Random()
# player2 = Player_MonteCarlo(10, rollout_player=player_rollout1)
run()


