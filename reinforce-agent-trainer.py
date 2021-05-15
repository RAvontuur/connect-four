from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tf_agents.agents.reinforce import reinforce_agent
from tf_agents.environments import tf_py_environment
from tf_agents.networks import actor_distribution_network
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common
from tf_agents.policies import policy_saver


from connect_four_py_env import ConnectFourPyEnv

tf.compat.v1.enable_v2_behavior()

num_iterations = 500  # @param {type:"integer"}
collect_episodes_per_iteration = 20  # @param {type:"integer"}
replay_buffer_capacity = 20000  # @param {type:"integer"}

fc_layer_params = (500,500,100)
dropout_layer_params = [{'rate' : 0.0}] * len(fc_layer_params)

learning_rate = 1e-4  # @param {type:"number"}
log_interval = 1  # @param {type:"integer"}
num_eval_episodes = 10  # @param {type:"integer"}
eval_interval = 20  # @param {type:"integer"}

train_py_env = ConnectFourPyEnv()
eval_py_env = ConnectFourPyEnv()


def collect_episode(environment: tf_py_environment.TFPyEnvironment, policy, num_episodes):
    episode_counter = 0
    environment.reset()

    while episode_counter < num_episodes:
        time_step = environment.current_time_step()
        action_step = policy.action(time_step)
        next_time_step = environment.step(action_step.action)
        traj = trajectory.from_transition(time_step, action_step, next_time_step)

        # Add trajectory to the replay buffer
        replay_buffer.add_batch(traj)

        if traj.is_boundary():
            episode_counter += 1


# This loop is so common in RL, that we provide standard implementations of
# these. For more details see the drivers module.


def compute_avg_return(environment, policy, num_episodes=10):
    total_return = 0.0
    for _ in range(num_episodes):

        time_step = environment.reset()
        episode_return = 0.0

        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = environment.step(action_step.action)
            episode_return += time_step.reward
        total_return += episode_return

    avg_return = total_return / num_episodes
    return avg_return.numpy()[0]


# Please also see the metrics module for standard implementations of different
# metrics.


train_env = tf_py_environment.TFPyEnvironment(train_py_env)
eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)

actor_net = actor_distribution_network.ActorDistributionNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    fc_layer_params=fc_layer_params, dropout_layer_params=dropout_layer_params)

optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

global_step = tf.compat.v1.train.get_or_create_global_step()
# train_step_counter = tf.compat.v2.Variable(0)

tf_agent = reinforce_agent.ReinforceAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    actor_network=actor_net,
    optimizer=optimizer,
    normalize_returns=True,
    train_step_counter=global_step)
tf_agent.initialize()

eval_policy = tf_agent.policy
collect_policy = tf_agent.collect_policy



replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=tf_agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=replay_buffer_capacity)

checkpoint_dir = 'checkpoint'
train_checkpointer = common.Checkpointer(
    ckpt_dir=checkpoint_dir,
    max_to_keep=1,
    agent=tf_agent,
    policy=tf_agent.policy,
    replay_buffer=replay_buffer,
    global_step=global_step
)
train_checkpointer.initialize_or_restore()
global_step = tf.compat.v1.train.get_or_create_global_step()

# (Optional) Optimize by wrapping some of the code in a graph using TF function.
tf_agent.train = common.function(tf_agent.train)

# Reset the train step
# tf_agent.train_step_counter.assign(0)

# Evaluate the agent's policy once before training.
avg_return = compute_avg_return(eval_env, tf_agent.policy, num_eval_episodes)
returns = [avg_return]

train_py_env.set_number_of_simulations(int(tf_agent.train_step_counter.numpy() / 30))

for _ in range(num_iterations):
    # Collect a few episodes using collect_policy and save to the replay buffer.
    collect_episode(
        train_env, tf_agent.collect_policy, collect_episodes_per_iteration)

    # Use data from the buffer and update the agent's network.
    experience = replay_buffer.gather_all()
    train_loss = tf_agent.train(experience)
    replay_buffer.clear()

    step = tf_agent.train_step_counter.numpy()

    if step % log_interval == 0:
        print('step = {0}: loss = {1}'.format(step, train_loss.loss))

    if step % eval_interval == 0:
        avg_return = compute_avg_return(eval_env, tf_agent.policy, num_eval_episodes)
        print('step = {0}: Average Return = {1}'.format(step, avg_return))
        returns.append(avg_return)
        train_checkpointer.save(global_step)
        tf_policy_saver = policy_saver.PolicySaver(tf_agent.policy)
        tf_policy_saver.save("policy")

    train_py_env.set_number_of_simulations(int(step / 100))

train_checkpointer.save(global_step)
tf_policy_saver = policy_saver.PolicySaver(tf_agent.policy)

tf_policy_saver.save("policy")
