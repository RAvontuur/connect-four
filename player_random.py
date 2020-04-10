import random
from environment import ConnectFourEnvironment
from player import Player


class PlayerRandom(Player):

    def action_values(self, env: ConnectFourEnvironment):
        result = [-1.0] * 7
        for a in env.get_legal_actions():
            result[a] = 0.0

        return result

    def play(self, env: ConnectFourEnvironment):
        assert (not env.terminated)

        free_columns = env.get_legal_actions()
        random.shuffle(free_columns)

        action = random.choice(free_columns)

        return env.move(action), action
