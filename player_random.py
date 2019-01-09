import random

class Player_Random:

    def __init__(self,  player):
        self.player = player

    def play(self, env):
        assert(env.next_to_move == self.player)
        assert(env.terminated == False)

        actions = env.get_legal_actions()
        action = random.choice(actions)

        return env.move(action)