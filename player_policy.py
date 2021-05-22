import numpy as np
import tensorflow as tf
from tf_agents.trajectories import time_step as ts

from environment import ConnectFourEnvironment
from player import Player


class PlayerPolicy(Player):

    def __init__(self, policy_dir):
        self.policy = tf.compat.v2.saved_model.load(policy_dir)

    def play(self, env: ConnectFourEnvironment, untried_actions=None):
        assert (not env.terminated)
        time_step = ts.TimeStep(step_type=tf.constant(value=[ts.StepType.MID], dtype=tf.int32),
                                observation=tf.constant(value=[env.state], dtype=tf.int64),
                                reward=tf.constant(value=[0.0], dtype=tf.float32),
                                discount=tf.constant(value=[0.0], dtype=tf.float32))
        action_step = self.policy.action(time_step)

        return env.move(action_step.action.numpy()[0]), action_step.action.numpy()[0]
