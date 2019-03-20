import random

class Player_One_Ahead():

    def play(self, env, untried_actions=None):
        assert(env.terminated == False)

        if untried_actions == None:
            free_columns = env.get_legal_actions()
            random.shuffle(free_columns)
        else:
            free_columns = untried_actions

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