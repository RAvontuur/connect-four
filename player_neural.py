import copy
import numpy as np
import tensorflow as tf

from qnetwork import Qnetwork


def processState(env):
    state = env.state

    if env.next_to_move == 1:
        X = np.array([1.0, 0.0])
        O = np.array([0.0, 1.0])
    else:
        O = np.array([1.0, 0.0])
        X = np.array([0.0, 1.0])

    neural_state = np.zeros(shape=(7, 6, 2), dtype=np.float32)
    for row in range(6):
        for col in range(7):
            if state[col][row] == 1:
                neural_state[col][row] = X
            elif state[col][row] == -1:
                neural_state[col][row] = O

    return np.reshape([neural_state], [7 * 6 * 2])



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

    def play(self, env, untried_actions=None):
        assert(env.terminated == False)

        s = processState(env)
        q_out = self.sess.run(self.mainQN.Qout, feed_dict={self.mainQN.scalarInput: [s]})[0]
        actions = q_out * (0.75 + 0.25 * np.random.random_sample((7,))) + 0.01 * np.random.random_sample((7,))

        # eliminate the tried actions
        if untried_actions is not None:
            for a in range(0,7):
                if a in untried_actions:
                    pass
                else:
                    actions[a] = -100000000.0

        action = np.argmax(actions)

        return env.move(action), action
