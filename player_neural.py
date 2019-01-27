import copy
import numpy as np
import tensorflow as tf

from qnetwork import Qnetwork


# This is a simple function to resize our game frames.
def processState(states):
    return np.reshape(states, [7 * 6 * 2])


def invert_state(state):
    X = np.array([1.0, 0.0])
    O = np.array([0.0, 1.0])

    state = copy.deepcopy(state)

    for row in range(6):
        for col in range(7):
            if np.all(state[0][col][row] == X):
                state[0][col][row] = O
            elif np.all(state[0][col][row] == O):
                state[0][col][row] = X
    return state


class Player_Neural:

    def __init__(self, sess = None, mainQN = None):
        if sess is None:
            path = "./dqn"  # The path to load our model from.

            tf.reset_default_graph()
            self.mainQN = Qnetwork()

            init = tf.global_variables_initializer()

            saver = tf.train.Saver()

            self.sess = tf.Session()
            self.sess.run(init)
            print('Loading Model...')
            ckpt = tf.train.get_checkpoint_state(path)
            saver.restore(self.sess, ckpt.model_checkpoint_path)
        else:
            self.sess = sess
            self.mainQN = mainQN

    def play(self, env):
        assert (env.terminated == False)

        state = env.state
        if env.next_to_move == -1:
            state = invert_state(state)

        s = processState(state)
        q_out = self.sess.run(self.mainQN.Qout, feed_dict={self.mainQN.scalarInput: [s]})[0]
        actions = q_out * (0.75 + 0.25 * np.random.random_sample((7,))) + 0.01 * np.random.random_sample((7,))
        action = np.argmax(actions)

        return env.move(action), action
