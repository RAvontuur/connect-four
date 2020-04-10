import random
from environment import ConnectFourEnvironment
from player import Player


class PlayerRandom(Player):

    def action_values(self, env: ConnectFourEnvironment):
        result = [-1.0] * 7
        for a in env.get_legal_actions():
            result[a] = 0.0

        return result

    def play(self, env: ConnectFourEnvironment, untried_actions = None):
        assert(not env.terminated)

        if untried_actions is None:
            free_columns = env.get_legal_actions()
            random.shuffle(free_columns)
        else:
            free_columns = untried_actions

        action = random.choice(free_columns)

        return env.move(action), action
