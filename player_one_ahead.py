import numpy as np
import random
import copy
from environment import ConnectFourEnvironment

class Player_One_Ahead():

    def __init__(self,  player):
        self.player = player
        self.play_level = 2

    def play(self, env):
        assert(env.next_to_move == self.player)
        assert(env.terminated == False)

        free_columns = []
        for col in range(7):
            if np.all(env.state[0][col][5] == ConnectFourEnvironment.EMPTY):
                free_columns.append(col)

        if self.play_level > 0:
            # try to find winning move
            for action1 in free_columns:
                env1 = copy.deepcopy(env)
                env2 = env1.move(action1)
                if env1.is_game_over():
                    if env1.game_result() > 0:
                        return env.move(action1)

                if self.play_level > 1:
                    # prevent opponent making a connect four
                    opponent_can_win = False
                    for action2 in free_columns:
                        env2.move(action2)
                        if env2.is_game_over():
                            if env2.game_result() > 0:
                                opponent_can_win = True
                                break

                    if not opponent_can_win:
                        return env.move(action1)


        action = random.choice(free_columns)
        return env.move(action)