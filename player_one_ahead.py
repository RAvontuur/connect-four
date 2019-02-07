import random

class Player_One_Ahead():

    def play(self, env):
        assert(env.terminated == False)

        free_columns = env.get_legal_actions()
        # for col in range(7):
        #     if env.state[col][5] == 0:
        #         free_columns.append(col)

        random.shuffle(free_columns)

        # try to find winning move
        for action1 in free_columns:
            if env.is_winning_action(env.next_to_move, action1):
                # print("lets win")
                return env.move(action1), action1

        # prevent opponent making a connect four if not doing action
        for action1 in free_columns:
            if env.is_winning_action(-env.next_to_move, action1):
                return env.move(action1), action1

        # prevent opponent making a connect four if doing action
        for action1 in free_columns:
            if not env.is_winning_action(-env.next_to_move, action1, row_offset=1):
                return env.move(action1), action1

        # print("random move")
        action = random.choice(free_columns)
        return env.move(action), action