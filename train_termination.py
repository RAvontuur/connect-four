from __future__ import absolute_import, division, print_function, unicode_literals

import csv

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from sum_pooling import GlobalSumPooling2D


def termination_model():
    kernel1 = np.zeros([4, 4, 2, 8])

    # horizontal (second row)
    for i in range(4):
        kernel1[1, i, 0, 0] = 1
        kernel1[1, i, 1, 4] = 1

    # vertical (second column)
    for i in range(4):
        kernel1[i, 1, 0, 1] = 1
        kernel1[i, 1, 1, 5] = 1

    # diagonal
    for i in range(4):
        kernel1[i, i, 0, 2] = 1
        kernel1[i, i, 1, 6] = 1

    # diagonal
    for i in range(4):
        kernel1[i, 3 - i, 0, 3] = 1
        kernel1[i, 3 - i, 1, 7] = 1

    bias1 = -3 * np.ones([8, 1])

    label1 = np.vstack((np.ones([4, 1]), np.zeros([4, 1])))
    label2 = np.vstack((np.zeros([4, 1]), np.ones([4, 1])))
    kernel2 = np.hstack((label1, label2))
    bias2 = np.zeros([2, 1])

    layer1 = layers.Conv2D(filters=8, kernel_size=(4, 4),
                           input_shape=(6, 7, 2), padding='same',
                           kernel_initializer=tf.constant_initializer(kernel1),
                           bias_initializer=tf.constant_initializer(bias1),
                           activation='relu')

    layer2 = GlobalSumPooling2D()
    layer3 = layers.Dense(2,
                          kernel_initializer=tf.constant_initializer(kernel2),
                          bias_initializer=tf.constant_initializer(bias2)
                          )
    return [layer1, layer2, layer3]


model = tf.keras.Sequential()

# for layer in termination_model():
# model.add(layer)
model.add(termination_model()[0])
model.add(termination_model()[1])
model.add(termination_model()[2])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='mse',
              metrics=['mae'])

model.summary()

file_name = 'rollouts-filtered.csv'

boards_train = []
labels_train = []

with open(file_name, newline='') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        labels_train.append(row[84:86])
        # -1: is empty +1: occupied -> 0: is empty +1: occupied
        boards_train.append((1 + np.array(row[0:84]))/2)

boards_train = np.reshape(boards_train, (len(boards_train), 6, 7, 2))

print(len(labels_train))

data = np.asarray(boards_train)
labels = np.asarray(labels_train)
print(boards_train[0].shape)
print(data.shape)

model.fit(data, labels, epochs=5, batch_size=256)
model.save("connect-four-positions-138-analytic-weights.h5")
