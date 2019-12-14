from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import csv

import tensorflow as tf
from tensorflow.keras import layers


def termination_model():
    kernel1 = np.zeros([84, 138])

    # horizontal (24x)
    for row in range(6):
        for col in range(4):
            for i in range(4):
                kernel1[2 * (col + i) + (14 * row), col + 4 * row] = 2
                kernel1[2 * (col + i) + (14 * row) + 1, 69 + col + 4 * row] = 2

    # vertical (21x)
    for row in range(3):
        for col in range(7):
            for i in range(4):
                kernel1[2 * col + 14 * (row + i), 24 + col + 7 * row] = 2
                kernel1[2 * col + 14 * (row + i) + 1, 24 + 69 + col + 7 * row] = 2

    # diagonal (12x)
    for row in range(3):
        for col in range(4):
            for i in range(4):
                kernel1[2 * (col + i) + 14 * (row + i), 45 + col + 4 * row] = 2
                kernel1[2 * (col + i) + 14 * (row + i) + 1, 45 + 69 + col + 4 * row] = 2

    # diagonal (12x)
    for row in range(3):
        for col in range(4):
            for i in range(4):
                kernel1[2 * (col + 3 - i) + 14 * (row + i), 57 + col + 4 * row] = 2
                kernel1[2 * (col + 3 - i) + 14 * (row + i) + 1, 57 + 69 + col + 4 * row] = 2


    # def plot_sums(i):
    #     print('---' + str(i) + '---' + str(np.sum(kernel1[0:84, i])))
    #
    #
    # def plot(i):
    #     print('---' + str(i) + '---')
    #     for row in range(6):
    #         start = 14 * row
    #         end = start + 14
    #         print(kernel1[start:end, i])
    #
    #
    # for i in range(138):
    #     plot(i)
    #
    # for i in range(138):
    #     plot_sums(i)

    bias1 = -7 * np.ones([138, 1])

    label1 = np.vstack((np.ones([69, 1]), np.zeros([69, 1])))
    label2 = np.vstack((np.zeros([69, 1]), np.ones([69, 1])))
    kernel2 = np.hstack((label1, label2))
    bias2 = np.zeros([2, 1])


    layer1 = layers.Dense(138, input_shape=(84,),
                           # kernel_initializer=tf.constant_initializer(kernel1),
                           # bias_initializer=tf.constant_initializer(bias1),
                           activation='relu')

    layer2 = layers.Dense(2,
                     # kernel_initializer=tf.constant_initializer(kernel2),
                     # bias_initializer=tf.constant_initializer(bias2)
    )
    return [layer1,layer2]


model = tf.keras.Sequential()

for layer in termination_model():
    model.add(layer)

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
        boards_train.append(row[0:84])

print(len(labels_train))

data = np.asarray(boards_train)
labels = np.asarray(labels_train)

model.fit(data, labels, epochs=500, batch_size=256)
model.save("connect-four-positions-138-analytic-weights.h5")
