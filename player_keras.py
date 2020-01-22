import numpy as np

from environment_keras import ConnectFourEnvironmentKeras


def convert_state(state):

    neural_state = -1 * np.ones(84, dtype=np.float32)
    for row in range(6):
        for col in range(7):
            if state[col][row] == 1:
                neural_state[2 * col + 14 * row] = 1
            elif state[col][row] == -1:
                neural_state[2 * col + 14 * row + 1] = 1

    return neural_state


class PlayerKeras:

    def __init__(self, number_of_simulations=10000):
        self.number_of_simulations = number_of_simulations
        self.env_keras = ConnectFourEnvironmentKeras(parallel_plays=number_of_simulations)

    def play(self, env, untried_actions=None):
        assert (not env.terminated)

        # copy state of env to env_keras
        self.env_keras.player = np.repeat([env.get_player()], self.number_of_simulations, axis=0)
        self.env_keras.state = np.repeat([convert_state(env.state)], self.number_of_simulations, axis=0)
        self.env_keras.reward = np.repeat([[0.0, 0.0]], self.number_of_simulations, axis=0)
        self.env_keras.terminated = np.repeat([0], self.number_of_simulations, axis=0)
        self.env_keras.illegal_action = np.repeat([0], self.number_of_simulations, axis=0)

        valid_action = np.zeros(14)
        offset = 0
        if env.get_player() == -1:
            offset = 1
        for col in env.get_legal_actions():
            valid_action[2*col + offset] = 1
        self.env_keras.valid_actions = np.repeat([valid_action], self.number_of_simulations, axis=0)

        # print("legal: {}".format(env.get_legal_actions()))
        # print("valid: {}".format(valid_action))

        # print("player {}".format(env.get_player()))
        # start roll-outs
        first_move = None
        next_move = np.zeros(self.number_of_simulations, dtype=int)
        counter = 1
        while np.any(self.env_keras.terminated == 0):
            # print("move-nr {}".format(counter))
            if counter > 50:
                print("maximum moves exceeded")
                break
            indices_tuple = np.nonzero(self.env_keras.valid_actions)
            # print("indices_tuple {}".format(indices_tuple[1]))
            permutation = np.random.permutation(indices_tuple[0].shape[0])
            next_move[indices_tuple[0][permutation]] = indices_tuple[1][permutation] / 2
            # print("next move {}".format(next_move))
            if first_move is None:
                first_move = next_move
            self.env_keras.move(next_move)
            counter += 1

        # gather statistics of all roll-outs
        histogram_first_move = np.histogram(first_move, np.arange(8))[0]
        # print("first move {}".format(first_move))
        # print(self.env_keras.illegal_action * self.env_keras.last_action * self.env_keras.player)
        print(histogram_first_move)
        # v = np.stack([first_move, self.env_keras.reward[:, 0], self.env_keras.reward[:, 1]], axis=1)
        # for i in range(self.number_of_simulations):
        #     print(v[i])
        histogram0_first_move = np.array(
            np.histogram(
                np.where(self.env_keras.reward[:, 0] > 0.5, first_move, -1),
                np.arange(8))[0],
            dtype=float)
        print(histogram0_first_move)
        histogram1_first_move = np.array(
            np.histogram(
                np.where(self.env_keras.reward[:, 1] > 0.5, first_move, -1),
                np.arange(8))[0],
            dtype=float)
        print(histogram1_first_move)
        # print(env.get_player())
        probabilities = 0.5 + 0.5 * (env.get_player() * (histogram0_first_move - histogram1_first_move)
                                     / (histogram_first_move + 0.001))
        probabilities = probabilities / np.sum(probabilities)
        print(probabilities)
        action = np.random.choice(7, p=probabilities)
        # action = np.argmax(probabilities)
        print("chosen action {}".format(action))
        return env.move(action), action
