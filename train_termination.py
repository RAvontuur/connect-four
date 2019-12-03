from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import csv

import tensorflow as tf
from tensorflow.keras import layers

model = tf.keras.Sequential()
model.add(layers.Dense(2*69, input_shape=(84,),
                       activation='relu'))
# Add a layer with 2 output units, no activation:
model.add(layers.Dense(2))

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
        labels_train.append(row[0:2])
        boards_train.append(row[2:86])

print(len(labels_train))

data = np.asarray(boards_train)
labels = np.asarray(labels_train)

model.fit(data, labels, epochs=300, batch_size=128)
model.save("connect-four-positions-138-no-activation.h5")

