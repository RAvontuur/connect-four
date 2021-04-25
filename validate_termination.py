from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import csv

from tensorflow import keras
from tensorflow.keras import layers

def run(file_name):

    boards_train = []
    labels_train = []

    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            labels_train.append(row[84:86])
            boards_train.append(row[0:84])

    print(len(labels_train))

    size = len(labels_train)

    data_predict = np.asarray(boards_train)
    labels_predict = np.asarray(labels_train)

    # model = keras.models.load_model('connect-four-positions-138.h5')
    # model = keras.models.load_model('connect-four-positions-138-no-activation-weights.h5')
    # model = keras.models.load_model('connect-four-positions-138-analytic-weights.h5', custom_objects={'ReLU': layers.ReLU})
    model = keras.models.load_model('connect-four-positions-138-analytic-weights.h5')
    result = np.reshape(model.predict(data_predict.reshape((size, 6, 7, 2)), batch_size=32), (size, 2))

    def plot(i):
        print(np.hstack((labels_predict,result))[i])
        print(data_predict[i, 0:14])
        print(data_predict[i, 14:28])
        print(data_predict[i, 28:42])
        print(data_predict[i, 42:56])
        print(data_predict[i, 56:70])
        print(data_predict[i, 70:84])
        print()

    j = 0
    plotted = 0
    for i in range(size):
        p = labels_predict[i]
        l = result[i]
        # print(str(i) + " " + str(p)  + " " + str(l))
        if (abs(p[0] - l[0]) < 0.5) and (abs(p[1] - l[1]) < 0.5):
            j+=1
        else:
            if plotted < 10:
                plot(i)
                plotted += 1

    print(str(j) + " good predictions, out of " + str(size))


run('rollouts-filtered.csv')
# run('rollouts.csv')