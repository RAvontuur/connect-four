import random

class Player_Random:

    def play(self, env):
        assert(env.terminated == False)

        actions = env.get_legal_actions()
        action = random.choice(actions)

        return env.move(action), action