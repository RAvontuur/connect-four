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
        super().__init__()
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int64, minimum=0, maximum=6, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(7, 6), dtype=np.int64, minimum=-1, maximum=1, name='observation')
        self._env = ConnectFourEnvironment()
        self._player_opponent = PlayerMonteCarlo(5, rollout_player=PlayerRandom())
        # self._player_assistant: PlayerMonteCarlo = PlayerMonteCarlo(1000, rollout_player=PlayerRandom())

    def set_number_of_simulations(self, n):
        # print("number of simulations: {}".format(n))
        self._player_opponent.number_of_simulations = n

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _to_observation(self, env):
        return env.state

    def _reset(self):
        self._env.restart()
        return ts.restart(self._to_observation(self._env))

    def _step(self, action):

        action_policy = action.min()
        if self._env.is_game_over():
            # The last action ended the episode. Ignore the current action and start
            # a new episode.
            return self.reset()

        # the player we train, is always starting
        assert(self._env.get_player() == 1)
        self._env.move(action_policy)

        if self._env.is_game_over():
            # print(self._env.display())
            reward = self._env.game_result(1)
            return ts.termination(self._to_observation(self._env), reward)

        # the player we challenge is a strong Monte Carlo Tree Search player
        assert (self._env.get_player() == -1)
        env, action = self._player_opponent.play(self._env)

        if env.is_game_over():
            # print(env.display())
            reward = env.game_result(1)
            self._env = env
            return ts.termination(self._to_observation(env), reward)
        else:
            # self._player_assistant.play(self._env)
            # reward = self._player_assistant.choices()[action_policy]
            reward = 0.05
            self._env = env
            return ts.transition(self._to_observation(env), reward=reward, discount=0.0)

