from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_neural import Player_Neural

number_of_plays = 100
show_play = False

i = 1

result_1 = 0.
result_2 = 0.

while i <= number_of_plays:
    print("play " + str(i) + " starts")
    env = ConnectFourEnvironment()

    player2 = Player_Neural(-1)
    # player1 = Player_MonteCarlo(1, 500)
    # player1 = Player_Random(1)
    player1 = Player_MonteCarlo(1, 1000)
    # player2 = Player_One_Ahead(-1, 2)

    while True:
        env = player1.play(env)
        if env.is_game_over():
            print(env)
            break

        env = player2.play(env)
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
    i += 1
