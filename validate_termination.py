from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import csv

from tensorflow import keras

def run(file_name):

    boards_train = []
    labels_train = []

    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            labels_train.append(row[0:2])
            boards_train.append(row[2:86])

    print(len(labels_train))

    size = 1000

    idxs = np.random.randint(len(labels_train), size=size)
    # idxs = range(size)
    boards_predict = [boards_train[i] for i in idxs]
    labels_predict = [labels_train[i] for i in idxs]

    data_predict = np.asarray(boards_predict)
    labels_predict = np.asarray(labels_predict)

    # model = keras.models.load_model('connect-four-positions-138.h5')
    model = keras.models.load_model('connect-four-positions-138-no-activation.h5')
    result = model.predict(data_predict, batch_size=32)

    print(np.hstack((labels_predict,result))[1:10])

    j = 0
    for i in range(size):
        p = labels_predict[i]
        l = result[i]
        # print(str(i) + " " + str(p)  + " " + str(l))
        if (abs(p[0] - l[0]) < 0.5) and (abs(p[1] - l[1]) < 0.5):
            j+=1
    print(str(j) + " good predictions, out of " + str(size))


run('rollouts-filtered.csv')
run('rollouts.csv')