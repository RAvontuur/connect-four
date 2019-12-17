from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import csv

import tensorflow as tf
from tensorflow.keras import layers


def termination_model():
    layer1 = layers.Dense(138, input_shape=(84,), activation='relu')
    layer2 = layers.Dense(2)
    model = tf.keras.Sequential()
    model.add(layer1)
    model.add(layer2)
    return model

def actions_model():
    layer = layers.Dense(84, input_shape=(98,),
                 activation='tanh')
    model = tf.keras.Sequential()
    model.add(layer)
    return model

def valid_moves_model():
    layer = layers.Dense(14, input_shape=(84,),
                 activation='relu')
    model = tf.keras.Sequential()
    model.add(layer)
    return model

board_input = layers.Input(shape=(84,))
action_input = layers.Input(shape=(14,))
board_output = actions_model()(layers.concatenate([board_input, action_input]))
valid_actions_output = valid_moves_model()(board_output)
reward_output = termination_model()(board_output)


model = tf.keras.Model(inputs=[board_input, action_input], outputs=[board_output, reward_output, valid_actions_output])


model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='mse',
              metrics=['mae'])

model.summary()

file_name = 'rollouts-filtered.csv'

board_data_train = []
actions_data_train = []
board_labels_train = []
reward_labels_train = []
valid_actions_labels_train = []

with open(file_name, newline='') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        board_data_train.append(row[0:84])
        actions_data_train.append(row[84:98])
        board_labels_train.append(row[98:182])
        reward_labels_train.append(row[182:184])
        valid_actions_labels_train.append(row[184:198])

print(len(reward_labels_train))

board_data = np.asarray(board_data_train)
action_data = np.asarray(actions_data_train)
board_labels = np.asarray(board_labels_train)
valid_actions_labels = np.asarray(valid_actions_labels_train)
reward_labels = np.asarray(reward_labels_train)

model.fit([board_data, action_data],
          [board_labels, reward_labels, valid_actions_labels],
          epochs=500, batch_size=256)
model.save("connect-four-environment.h5")
