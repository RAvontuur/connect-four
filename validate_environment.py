from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import csv

from tensorflow import keras
from tensorflow.keras import layers

def run(file_name):

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

    size = len(reward_labels_train)

    board_data_predict = np.asarray(board_data_train)
    actions_data_predict = np.asarray(actions_data_train)
    board_labels_predict = np.asarray(board_labels_train)
    reward_labels_predict = np.asarray(reward_labels_train)
    valid_actions_labels_predict = np.asarray(valid_actions_labels_train)

    model = keras.models.load_model('connect-four-environment.h5')
    [board, rewards, valid_actions] = model.predict([board_data_predict, actions_data_predict], batch_size=32)

    def plot(i):
        print(np.hstack((reward_labels_predict,rewards))[i])
        print(board_labels_predict[i, 0:14])
        print(board_labels_predict[i, 14:28])
        print(board_labels_predict[i, 28:42])
        print(board_labels_predict[i, 42:56])
        print(board_labels_predict[i, 56:70])
        print(board_labels_predict[i, 70:84])
        print()

    j = 0
    plotted = 0
    for i in range(size):
        p = reward_labels_predict[i]
        l = rewards[i]
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