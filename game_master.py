import time
from environment import ConnectFourEnvironment
from player_montecarlo import PlayerMonteCarlo
from player_random import PlayerRandom

number_of_plays = 100
show_play = True
show_final_play = True
show_intermediate_result = True
show_analyzed_play = True

def run():
    result_1 = 0.
    result_2 = 0.

    i = 1
    start_tot = 0
    while i <= number_of_plays:
        start = time.time() * 1000
        if show_intermediate_result:
            print("play " + str(i) + " starts")
        env: ConnectFourEnvironment = ConnectFourEnvironment()

        while True:
            assert(env.get_player() == 1)
            env, action = player1.play(env)
            if env.is_game_over():
                if show_final_play:
                    print(env)
                break
            if show_analyzed_play and player1.analyzed_result() is not None:
                print("analyzed result: {}".format(player1.analyzed_result()))
                print(env)

            assert(env.get_player() == -1)
            env, action = player2.play(env)
            if env.is_game_over():
                if show_final_play:
                    print(env)
                break
            if show_analyzed_play and player2.analyzed_result() is not None:
                print("analyzed result: {}".format(player2.analyzed_result()))
                print(env)

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

    print("took (ms): " + str(start_tot/(i-1)))


print("starting")
player1 = PlayerMonteCarlo(7, rollout_player=PlayerRandom())
# player2 = PlayerMonteCarlo(100, rollout_player=PlayerRandom())
player2 = PlayerRandom()
run()


