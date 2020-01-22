import random


class Player_Random:

    def play(self, env, untried_actions = None):
        assert(not env.terminated)

        if untried_actions is None:
            free_columns = env.get_legal_actions()
            random.shuffle(free_columns)
        else:
            free_columns = untried_actions

        action = random.choice(free_columns)

        return env.move(action), action