from __future__ import absolute_import, division, print_function, unicode_literals

import csv

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import regularizers

from sum_pooling import GlobalSumPooling2D


def load_data(file_name):
    boards_train = []
    labels_train = []

    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            labels_train.append(row[84:86])
            # -1: is empty +1: occupied -> 0: is empty +1: occupied
            boards_train.append((1 + np.array(row[0:84])) / 2)

    boards_train = np.reshape(boards_train, (len(boards_train), 6, 7, 2))

    print(len(labels_train))

    data = np.asarray(boards_train)
    labels = np.asarray(labels_train)
    print(boards_train[0].shape)
    print(data.shape)
    return data, labels


def termination_model(alfa=1.0, l2=0):
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

    layer1 = layers.Conv2D(filters=16, kernel_size=(4, 4),
                           input_shape=(6, 7, 2),
                           kernel_regularizer=regularizers.l2(l2),
                           # kernel_initializer=tf.constant_initializer(kernel1),
                           # bias_initializer=tf.constant_initializer(bias1),
                           padding='same'
                           )

    layer2 = layers.LeakyReLU(alpha=alfa)
    # layer2 = layers.ReLU()
    layer3 = GlobalSumPooling2D()
    layer4 = layers.Dense(2,
                          # activation='relu',
                          # kernel_initializer=tf.constant_initializer(kernel2),
                          # bias_initializer=tf.constant_initializer(bias2)
                          )
    # layer4.trainable = False
    return [layer1, layer2, layer3, layer4]


def create_model(alfa, l2):
    model = tf.keras.Sequential()

    for layer in termination_model(alfa=alfa, l2=l2):
        print(layer)
        model.add(layer)

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='mse',
                  metrics=['mae'])
    return model


[data, labels] = load_data('rollouts-filtered.csv')

first_time = True
alfa = 1.0
l2 = 0.01
for i in range(20):
    print("i: {}, alfa: {}, l2: {}".format(i, alfa, l2))
    model = create_model(alfa=alfa, l2=l2)
    if not first_time:
        model.load_weights("temp.h5")
    model.fit(data, labels, epochs=5, batch_size=256)
    model.save("temp.h5")
    first_time = False
    alfa = alfa / 5
    l2 = l2 / 1.5
    if i > 15:
        alfa = 0
        l2 = 0

# model = create_model(alfa=0, l2=0)
# model.load_weights("temp.h5")
# model.fit(data, labels, epochs=20, batch_size=256)

model.save("connect-four-positions-138-analytic-weights.h5")
