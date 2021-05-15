from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts

from environment import ConnectFourEnvironment
from player_montecarlo import PlayerMonteCarlo
from player_random import PlayerRandom

tf.compat.v1.enable_v2_behavior()


class ConnectFourPyEnv(py_environment.PyEnvironment):

    def __init__(self):
        self._action_spec = array_spec.BoundedArraySpec(
            shape=[1], dtype=np.int64, minimum=0, maximum=6, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(7, 6), dtype=np.int64, minimum=-1, maximum=1, name='observation')
        self._env = ConnectFourEnvironment()
        self._player_opponent = PlayerMonteCarlo(10, rollout_player=PlayerRandom())

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _to_observation(self):
        return self._env.state

    def _reset(self):
        print("reset")
        self._env.restart()
        return ts.restart(self._to_observation())

    def _step(self, action):

        if self._env.is_game_over():
            # The last action ended the episode. Ignore the current action and start
            # a new episode.
            return self.reset()

        # the player we train, is always starting
        print("action: {}".format(action[0]))
        assert(self._env.get_player() == 1)
        self._env.move(action[0])

        if self._env.is_game_over():
            print(self._env.display())
            reward = self._env.game_result(1)
            return ts.termination(self._to_observation(), reward)

        # the player we challenge is a strong Monte Carlo Tree Search player
        assert (self._env.get_player() == -1)
        env, action = self._player_opponent.play(self._env)
        self._env = env

        if self._env.is_game_over():
            print(self._env.display())
            reward = self._env.game_result(1)
            return ts.termination(self._to_observation(), reward)
        else:
            return ts.transition(self._to_observation(), reward=0.1, discount=0.0)
