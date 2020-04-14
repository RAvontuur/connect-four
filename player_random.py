import random
from environment import ConnectFourEnvironment
from player import Player


class PlayerRandom(Player):

    def prior_values(self, env: ConnectFourEnvironment):
        result = [1000.0] * len(env.get_legal_actions())
        return result

    def play(self, env: ConnectFourEnvironment):
        assert(not env.terminated)

        free_columns = env.get_legal_actions()
        random.shuffle(free_columns)
        action = random.choice(free_columns)

        return env.move(action), action
