import numpy as np
import random
from environment import ConnectFourEnvironment

class Player_One_Ahead():

    def __init__(self, play_level=2):
        self.play_level = play_level

    def play(self, env):
        assert(env.terminated == False)

        free_columns = []
        for col in range(7):
            if np.all(env.state[0][col][5] == ConnectFourEnvironment.EMPTY):
                free_columns.append(col)

        random.shuffle(free_columns)

        if self.play_level > 0:
            # try to find winning move
            for action1 in free_columns:
                env1 = env.move(action1)
                if env1.is_game_over():
                    if env1.game_result(env.next_to_move) > 0:
                        # print("lets win")
                        return env.move(action1), action1

                if self.play_level > 1:
                    # prevent opponent making a connect four
                    opponent_can_win = False
                    for action2 in free_columns:
                        env2 = env1.move(action2)
                        if env2.is_game_over():
                            if env2.game_result(env1.next_to_move) > 0:
                                opponent_can_win = True
                                break

                    if not opponent_can_win:
                        # print("opponent can not win")
                        return env.move(action1), action1

        # print("random move")
        action = random.choice(free_columns)
        return env.move(action), action